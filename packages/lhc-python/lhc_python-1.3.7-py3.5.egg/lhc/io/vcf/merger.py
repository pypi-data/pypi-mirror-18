import re

from collections import OrderedDict, defaultdict, Counter
from functools import reduce

from operator import add
from lhc.binf.genomic_coordinate import GenomicPosition as Position
from sortedcontainers import SortedDict


class VcfMerger(object):
    
    CHR_REGX = re.compile('\d+$|X$|Y$|M$')
    
    def __init__(self, iterators, bams=None, key=None):
        bams = bams if bams else []
        self.iterators = iterators
        self.key = key
        hdrs = [it.header for it in self.iterators]
        self.hdrs = self._merge_headers(hdrs)
        self.samples = reduce(add, (it.samples for it in self.iterators))
        if bams is None or len(bams) == 0:
            self.bams = []
            self.sample_to_bam = {}
        else:
            import pysam
            self.bams = []
            self.sample_to_bam = {}
            for bam_name in bams:
                bam = pysam.Samfile(bam_name)
                sample = bam.header['RG'][0]['SM'].strip()
                if sample in self.samples:
                    self.bams.append(bam)
                    self.sample_to_bam[sample] = bam
                else:
                    bam.close()

    def __iter__(self):
        """ Iterate through merged vcf_ lines.

        TODO: phased genotypes aren't handled
        """
        tops = [next(iterator) for iterator in self.iterators]
        sorted_tops = self._init_sorting(tops)

        while len(sorted_tops) > 0:
            key, idxs = sorted_tops.popitem(last=False)

            # REF
            ref = sorted((tops[idx].data['ref'] for idx in idxs), key=lambda x: len(x))[-1]

            # ALT
            alt = set()
            sample_to_top = {}
            for idx in idxs:
                top = tops[idx]
                top_alt = [a + ref[len(top.data['ref']):] for a in top.data['alt']]
                alt.update(top_alt)
                for sample in top.data['samples']:
                    sample_to_top[sample] = (top, top_alt)
            alt = sorted(alt)

            # INFO
            info = defaultdict(set)
            for idx in idxs:
                top = tops[idx]
                for key, value in top.data['info'].items():
                    info[key].add(value)
            move_to_sample = set(key for key in info if len(info[key]) > 1)
            for key in move_to_sample:
                del info[key]
            
            format_ = {key: '' for key in move_to_sample}
            samples = {}
            for sample_name in self.samples:
                if sample_name in sample_to_top:
                    top, top_alt = sample_to_top[sample_name]
                    sample_data = top.data['samples'][sample_name]
                    if 'Q' not in format_:
                        format_['Q'] = ''
                    if 'GT' not in format_:
                        format_['GT'] = '0/0'
                    qual = sample_data['Q'] if 'Q' in sample_data else\
                        None if top.data['qual'] is None else\
                        top.data['qual']
                    samples[sample_name] = {'Q': qual}
                    samples[sample_name]['GT'] =\
                        self._get_gt(sample_data['GT'], top_alt, alt) if 'GT' in sample_data else\
                        './.'
                    if 'GQ' in sample_data:
                        if 'GQ' not in format_:
                            format_['GQ'] = ''
                        samples[sample_name]['GQ'] = sample_data['GQ']
                    if 'RO' in sample_data:
                        if 'RO' not in format_:
                            format_['RO'] = '0'
                        if 'AO' not in format_:
                            format_['AO'] = ','.join('0' * len(alt))
                        if 'AF' not in format_:
                            format_['AF'] = '0'
                        samples[sample_name]['RO'] = sample_data['RO']
                        samples[sample_name]['AO'] = self._get_ao(sample_data['AO'], top.data['alt'], alt)
                        if samples[sample_name]['AO'] is None or samples[sample_name]['RO'] is None:
                            continue
                        ro = float(samples[sample_name]['RO'])
                        aos = [float(ao) for ao in samples[sample_name]['AO'].split(',')]
                        afs = [ao / (ro + ao) if ro + ao > 0 else 0 for ao in aos]
                        samples[sample_name]['AF'] = ','.join('{:.3f}'.format(af) for af in afs)
                elif sample_name in self.sample_to_bam:
                    if 'GT' not in format_:
                        format_['GT'] = '0/0'
                    if 'RO' not in format_:
                        format_['RO'] = '0'
                    if 'AO' not in format_:
                        format_['AO'] = ','.join('0' * len(alt))
                    if 'AF' not in format_:
                        format_['AF'] = '0'
                    ro, aos = self._get_depth(sample_name, tops[idxs[0]].chromosome, tops[idxs[0]].pos, ref, alt)
                    samples[sample_name] = {'.': '.'} if ro is None else {
                        'RO': ro,
                        'AO': aos,
                    }
                    if ro is None or aos is None:
                        continue
                    ro = float(ro)
                    aos = [float(ao) for ao in aos.split(',')]
                    afs = [ao / (ro + ao) if ro + ao > 0 else 0 for ao in aos]
                    samples[sample_name]['AF'] = ','.join('{:.3f}'.format(af) for af in afs)
                else:
                    samples[sample_name] = {}

            for fmt, default in format_.items():
                for sample in samples.values():
                    if fmt not in sample:
                        sample[fmt] = default

            # INFO (2)
            for idx in idxs:
                iterator = self.iterators[idx]
                if len(iterator.samples) > 1:
                    break
                sample = iterator.samples[0]
                for key, value in tops[idx].data['info'].items():
                    if key in move_to_sample:
                        samples[sample][key] = value

            # QUAL
            qual = None if any(tops[idx].data['qual'] is None for idx in idxs) else\
                min(tops[idx].data['qual'] for idx in idxs)

            yield Position(tops[idxs[0]].chromosome, tops[idxs[0]].position, data={
                'id': tops[idxs[0]].data['id'],
                'ref': ref,
                'alt': alt,
                'qual': qual,
                'filter': '.',
                'info': info,
                'format': sorted(format_),
                'samples': samples
            })

            for idx in idxs:
                try:
                    tops[idx] = next(self.iterators[idx])
                    self._update_sorting(sorted_tops, tops[idx], idx)
                except StopIteration:
                    pass
    
    def _init_sorting(self, tops):
        sorted_tops = SortedDict(self.key)
        for idx, entry in enumerate(tops):
            self._update_sorting(sorted_tops, entry, idx)
        return sorted_tops
    
    def _update_sorting(self, sorted_tops, entry, idx):
        if entry not in sorted_tops:
            sorted_tops[entry] = []
        sorted_tops[entry].append(idx)
    
    def _merge_headers(self, hdrs):
        all_keys = defaultdict(list)
        for hdr in hdrs:
            for i, key in enumerate(hdr):
                all_keys[key].append(i)
        res = OrderedDict()
        for k, v in sorted(iter(all_keys.items()), key=lambda item: sum(item[1])):
            values = OrderedDict()
            for hdr in hdrs:
                if k in hdr:
                    values.update((value, None) for value in hdr[k])
            res[k] = list(values)
        return res
    
    def _get_gt(self, gt, old_alt, new_alt):
        try:
            a1, a2 = list(map(int, gt.split('/')))
        except ValueError:
            return './.'
        a1 = new_alt.index(old_alt[a1 - 1]) + 1 if 0 < a1 <= len(old_alt) else 0
        a2 = new_alt.index(old_alt[a2 - 1]) + 1 if 0 < a2 <= len(old_alt) else 0
        return '{}/{}'.format(a1, a2)
    
    def _get_ao(self, ao, old_alt, new_alt):
        res = {k: v for k, v in zip(old_alt, ao.split(','))}
        return ','.join(res[a] if a in res else '0' for a in new_alt)
    
    def _get_depth(self, sample, chr, pos, ref, alt):
        bam = self.sample_to_bam[sample]
        ref_start = pos
        ref_stop = pos + len(ref)
        cnt = Counter()
        for read in bam.fetch(chr, ref_start, ref_stop):
            read_start, read_stop, truncated =\
                self._get_read_interval(read, ref_start, ref_stop)
            alt_seq = read.seq[read_start:read_stop]
            if truncated:  # assume reference
                alt_seq += ref[len(alt_seq):]
            cnt[alt_seq] += 1
        if cnt[ref] == 0 and all(cnt[a] == 0 for a in alt):
            return None, None
        return str(cnt[ref]), ','.join(str(cnt[a]) for a in alt)
    
    def _get_read_interval(self, read, ref_start, ref_stop):
        read_start = 0
        ref_pos = 0
        truncated = True
        read_pos = read.qstart
        for op, length in read.cigar:
            read_ext = [1, 1, 0, 1, 1, 1, 1, 1, 1][op] * length
            ref_ext = [1, 0, 1, 1, 1, 1, 1, 1, 1][op] * length
            if read.pos + ref_pos + ref_ext > ref_start and read_start == 0:
                read_start = read_pos + (ref_start - ref_pos - read.pos)
            if read.pos + ref_pos + ref_ext > ref_stop:
                truncated = False
                break
            read_pos += read_ext
            ref_pos += ref_ext
        read_stop = read_pos + (ref_stop - ref_pos - read.pos)
        return read_start, read_stop, truncated
