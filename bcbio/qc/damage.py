"""Provide summary details on damage filtering for MultiQC.
"""
import os

from bcbio import utils
from bcbio.distributed.transaction import file_transaction
from bcbio.pipeline import datadict as dd
from bcbio.provenance import do
from bcbio.qc import variant

def run(bam_file, data, out_dir):
    out = {}
    vcinfo = variant.get_active_vcinfo(data)
    if vcinfo:
        out_file = os.path.join(utils.safe_makedir(out_dir),
                                "%s-damage.yaml" % (dd.get_sample_name(data)))
        if not utils.file_exists(out_file):
            with file_transaction(data, out_file) as tx_out_file:
                cmd = ["dkfzbiasfilter_summarize.py", "--sample=%s" % dd.get_sample_name(data),
                       "--outfile=%s" % tx_out_file, vcinfo["vrn_file"]]
                do.run(cmd, "Summarize damage filtering")
        if utils.file_exists(out_file):
            out["base"] = out_file
    return out
