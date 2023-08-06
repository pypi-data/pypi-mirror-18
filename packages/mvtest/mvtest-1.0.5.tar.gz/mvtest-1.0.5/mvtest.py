#!/usr/bin/env python


__author__ = 'torstees'
__copyright__ = "Copyright (C) 2015 Todd Edwards, Chun Li and Eric Torstenson"
__license__ = "GPL3.0"
#     This file is part of MVtest.
#
#     MVtest is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     MVtest is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with MVtest.  If not, see <http://www.gnu.org/licenses/>.


import argparse
import sys
import numpy
import scipy
import os
import libgwas
import meanvar
from libgwas.data_parser import DataParser
from libgwas.boundary import BoundaryCheck
from libgwas.snp_boundary_check import SnpBoundaryCheck
from libgwas.exceptions import InvalidBoundarySpec
from libgwas.pheno_covar import PhenoCovar
from libgwas.exceptions import ReportableException
import libgwas.pedigree_parser as pedigree_parser
import libgwas.transposed_pedigree_parser as transposed_pedigree_parser
import libgwas.bed_parser as bed_parser
import meanvar.mv_esteq as mv_esteq
from libgwas import BuildReportLine
from libgwas import impute_parser
from libgwas import mach_parser
import libgwas.standardizer
import meanvar.mvstandardizer
from libgwas import ExitIf

__version__ = meanvar.__version__

ExitIf("mvtest.py requires python 2.7.x  to run", sys.version_info < (2,7))

libgwas.standardizer.set_standardizer(meanvar.mvstandardizer.Standardizer)

"""usage: mvtest.py [-h] [-v] [--vall] [--chr N] [--snps SNPS] [--from-bp START]
                 [--to-bp END] [--from-kb START] [--to-kb END]
                 [--from-mb START] [--to-mb END] [--exclude EXCLUDE]
                 [--keep KEEP] [--remove REMOVE] [--file FILE] [--ped PED]
                 [--map MAP] [--map3] [--no-sex] [--no-parents] [--no-fid]
                 [--no-pheno] [--liability] [--bfile BFILE] [--bed BED]
                 [--bim BIM] [--fam FAM] [--tfile TFILE] [--tped TPED]
                 [--tfam TFAM] [--compressed] [--impute IMPUTE]
                 [--impute-fam IMPUTE_FAM] [--impute-offset IMPUTE_OFFSET]
                 [--impute-count IMPUTE_COUNT] [--impute-uncompressed]
                 [--impute-encoding {additive,dominant,recessive,genotype}]
                 [--impute-info-ext IMPUTE_INFO_EXT]
                 [--impute-gen-ext IMPUTE_GEN_EXT]
                 [--impute-info-thresh IMPUTE_INFO_THRESH] [--mach MACH]
                 [--mach-offset MACH_OFFSET] [--mach-count MACH_COUNT]
                 [--mach-uncompressed] [--mach-chunk-size MACH_CHUNK_SIZE]
                 [--mach-info-ext MACH_INFO_EXT]
                 [--mach-dose-ext MACH_DOSE_EXT]
                 [--mach-min-rsquared MACH_MIN_RSQUARED] [--pheno PHENO]
                 [--sample-pheno SAMPLE_PHENO] [--mphenos MPHENOS]
                 [--pheno-names PHENO_NAMES] [--all-pheno] [--covar COVAR]
                 [--sample-covar SAMPLE_COVAR] [--covar-numbers COVAR_NUMBERS]
                 [--covar-names COVAR_NAMES] [--sex]
                 [--missing-phenotype MISSING_PHENOTYPE] [--maf MAF]
                 [--max-maf MAX_MAF] [--geno GENO] [--mind MIND] [--verbose]

MV Test: 1.0.0rc5

optional arguments:
  -h, --help            show this help message and exit
  -v                    Print version number
  --vall                Print version number along with each dependency
  --chr N               Select Chromosome
  --snps SNPS           Comma-delimited list of SNP(s): rs1,rs2,rs3-rs6
  --from-bp START       SNP range start
  --to-bp END           SNP range end
  --from-kb START       SNP range start
  --to-kb END           SNP range end
  --from-mb START       SNP range start
  --to-mb END           SNP range end
  --exclude EXCLUDE     Comma-delimited list of rsids to be excluded
  --keep KEEP           Comma-delimited list of individuals to be analyzed
  --remove REMOVE       Comma-delimited list of individuals to be removed from
                        analysis
  --file FILE           Prefix for .ped and .map files
  --ped PED             PLINK compatible .ped file
  --map MAP             PLINK compatible .map file
  --map3                MAP file has only 3 columns
  --no-sex              Pedigree file doesn't have column 5 (sex)
  --no-parents          Pedigree file doesn't have columns 3 and 4 (parents)
  --no-fid              Pedigree file doesn't have column 1 (family ID)
  --no-pheno            Pedigree file doesn't have column 6 (phenotype
  --liability           Pedigree file has column 7 (liability)
  --bfile BFILE         Prefix for .bed, .bim and .fam files
  --bed BED             Binary Ped file (.bed)
  --bim BIM             Binary ped marker file (.bim)
  --fam FAM             Binary ped family file (.fam)
  --tfile TFILE         Prefix for .tped and .tfam files
  --tped TPED           Transposed Pedigree file (.tped)
  --tfam TFAM           Transposed pedigre Family file (.tfam)
  --compressed          Ped/TPed compressed with gzip (named .ped.tgz or
                        .tped.tgz)
  --impute IMPUTE       File containing list of impute output for analysis
  --impute-fam IMPUTE_FAM
                        File containing family details for impute data
  --impute-offset IMPUTE_OFFSET
                        Impute file index (1 based) to begin analysis
  --impute-count IMPUTE_COUNT
                        Number of impute files to process (for this node)
  --impute-uncompressed
                        Indicate that the impute input is not gzipped, but
                        plain text
  --impute-encoding {additive,dominant,recessive,genotype}
                        Genetic model to be used
  --impute-info-ext IMPUTE_INFO_EXT
                        Portion of filename denotes info filename
  --impute-gen-ext IMPUTE_GEN_EXT
                        Portion of filename that denotes gen file
  --impute-info-thresh IMPUTE_INFO_THRESH
                        Threshold for filtering imputed SNPs with poor 'info'
                        values
  --mach MACH           File containing list of MACH output for analysis
  --mach-offset MACH_OFFSET
                        Mach file index (1 based) to begin analysis
  --mach-count MACH_COUNT
                        Number of mach files to process (for this node)
  --mach-uncompressed   Indicate that the mach input is not gzipped
  --mach-chunk-size MACH_CHUNK_SIZE
                        Max number of loci to load at once (higher increases
                        memory requirements with some speed benefits)
  --mach-info-ext MACH_INFO_EXT
                        Portion of filename denotes info filenames
  --mach-dose-ext MACH_DOSE_EXT
                        Portion of filename that denotes dose files
  --mach-min-rsquared MACH_MIN_RSQUARED
                        Filter out loci with RSquared < this value
  --pheno PHENO         File containing phenotypes
  --sample-pheno SAMPLE_PHENO
                        (Mach) Sample file containing phenotypes
  --mphenos MPHENOS     Column number(s) for phenotype to be analyzed if
                        number of columns > 1
  --pheno-names PHENO_NAMES
                        Name for phenotype(s) to be analyzed (must be in
                        --pheno file)
  --all-pheno           Analyze all columns from the phenotype file
  --covar COVAR         File containing covariates
  --sample-covar SAMPLE_COVAR
                        (Mach) Sample file containing covariates
  --covar-numbers COVAR_NUMBERS
                        Comma-separated list of covariate indices
  --covar-names COVAR_NAMES
                        Comma-separated list of covariate names
  --sex                 Use sex from the pedigree file as a covariate
  --missing-phenotype MISSING_PHENOTYPE
                        Encoding for missing phenotypes
  --maf MAF             Minimum MAF allowed for analysis
  --max-maf MAX_MAF     MAX MAF allowed for analysis
  --geno GENO           MAX per-SNP missing for analysis
  --mind MIND           MAX per-person missing
  --verbose             Output additional data details

mvtest.py is uses many of the same arguments as plink, but there are a few
differences, so please consider the list above carefully.
"""

verbose_report = False

def ParseIndList(ids):
    id_list = []
    if os.path.isfile(ids):
        file = open(ids)
        for line in file:
            words = line.strip().split()
            ExitIf("%s:%s Individual file lists must contain " % (line.strip(), len(words)) +
                   "(exactly 2 columns (first two from ped columns)", len(words) != 2 )

            id_list.append(":".join(words[0:2]))
    else:
        id_list = ids.split(",")

    return id_list

class MVTestApplication(object):
    """Basic application wrapper.

    Parses the command line and sets the various flags associated with
    the user's preference and then reports the final settings in use.

    """

    def LoadCmdLine(self, args=sys.argv[1:]):
        """Parse user arguments using argparse and set up components"""
        parser = argparse.ArgumentParser(description="MV Test: " + __version__, epilog="""
mvtest.py is uses many of the same arguments as plink, but there are a few
differences, so please consider the list above carefully.
        """)

        parser.add_argument("-v", action='store_true', help="Print version number")
        parser.add_argument("--vall", action='store_true', help="Print version number along with each dependency")

        parser.add_argument("--chr", type=int, default=-1, metavar="N", help="Select Chromosome")
        parser.add_argument("--snps", type=str, default="", help="Comma-delimited list of SNP(s): rs1,rs2,rs3-rs6")
        parser.add_argument("--from-bp", type=int, metavar="START", help="SNP range start")
        parser.add_argument("--to-bp", type=int, metavar="END", help="SNP range end")
        parser.add_argument("--from-kb", type=int, metavar="START", help="SNP range start")
        parser.add_argument("--to-kb", type=int, metavar="END", help="SNP range end")
        parser.add_argument("--from-mb", type=int, metavar="START", help="SNP range start")
        parser.add_argument("--to-mb", type=int, metavar="END", help="SNP range end")
        parser.add_argument("--exclude", type=str, default="", help="Comma-delimited list of rsids to be excluded")

        # For now, I'm not implementing keep, since we don't have any real meaningful need for analyzing individuals
        # PLINK does, but we don't do the QC stuff they do.
        parser.add_argument("--keep", type=str, default="", help="Comma-delimited list of individuals to be analyzed")
        parser.add_argument("--remove", type=str, default="", help="Comma-delimited list of individuals to be removed from analysis")

        parser.add_argument("--file", type=str, help="Prefix for .ped and .map files")
        parser.add_argument("--ped", type=argparse.FileType('r'), help="PLINK compatible .ped file")
        parser.add_argument("--map", type=argparse.FileType('r'), help="PLINK compatible .map file")
        parser.add_argument("--map3", action='store_true', help="MAP file has only 3 columns")
        parser.add_argument("--no-sex", action='store_true', help="Pedigree file doesn't have column 5 (sex)")
        parser.add_argument("--no-parents", action="store_true", help="Pedigree file doesn't have columns 3 and 4 (parents)")
        parser.add_argument("--no-fid", action="store_true", help="Pedigree file doesn't have column 1 (family ID)")
        parser.add_argument("--no-pheno", action="store_true", help="Pedigree file doesn't have column 6 (phenotype")
        parser.add_argument("--liability", action="store_true", help="Pedigree file has column 7 (liability)")

        parser.add_argument("--bfile", type=str, help="Prefix for .bed, .bim and .fam files")
        parser.add_argument("--bed", type=argparse.FileType('r'), help="Binary Ped file (.bed)")
        parser.add_argument("--bim", type=argparse.FileType('r'), help="Binary ped marker file (.bim)")
        parser.add_argument("--fam", type=argparse.FileType('r'), help="Binary ped family file (.fam)")

        parser.add_argument("--tfile", type=str, help="Prefix for .tped and .tfam files")
        parser.add_argument("--tped", type=argparse.FileType('r'), help="Transposed Pedigree file (.tped)")
        parser.add_argument("--tfam", type=argparse.FileType('r'), help="Transposed pedigre Family file (.tfam)")
        parser.add_argument("--compressed", action="store_true", help="Ped/TPed compressed with gzip (named .ped.tgz or .tped.tgz)")

        parser.add_argument("--impute", type=argparse.FileType('r'), help="File containing list of impute output for analysis")
        parser.add_argument("--impute-fam", type=argparse.FileType('r'), help="File containing family details for impute data")
        parser.add_argument("--impute-offset", type=int, default=-1, help="Impute file index (1 based) to begin analysis")
        parser.add_argument("--impute-count", type=int, default=-1, help="Number of impute files to process (for this node)")
        parser.add_argument("--impute-uncompressed", action="store_true", help="Indicate that the impute input is not gzipped, but plain text")
        parser.add_argument("--impute-encoding", type=str, choices=['additive', 'dominant', 'recessive', 'genotype'], default='additive', help='Genetic model to be used')
        parser.add_argument("--impute-info-ext", type=str, default='info', help="Portion of filename denotes info filename")
        parser.add_argument("--impute-gen-ext", type=str, default='gen.gz', help="Portion of filename that denotes gen file")
        parser.add_argument("--impute-info-thresh", type=float, default=0.4, help="Threshold for filtering imputed SNPs with poor 'info' values")

        parser.add_argument("--mach", type=argparse.FileType('r'), help="File containing list of MACH output for analysis")
        parser.add_argument("--mach-offset", type=int, default=-1, help="Mach file index (1 based) to begin analysis")
        parser.add_argument("--mach-count", type=int, default=-1, help="Number of mach files to process (for this node)")
        parser.add_argument("--mach-uncompressed", action="store_true", help="Indicate that the mach input is not gzipped")
        parser.add_argument("--mach-chunk-size", type=int, default=100000, help="Max number of loci to load at once (higher increases memory requirements with some speed benefits)")
        parser.add_argument("--mach-info-ext", type=str, default="info.gz", help="Portion of filename denotes info filenames")
        parser.add_argument("--mach-dose-ext", type=str, default="dose.gz", help="Portion of filename that denotes dose files")
        parser.add_argument("--mach-min-rsquared", type=float, default=0.3, help="Filter out loci with RSquared < this value")
        parser.add_argument("--mach-chrpos", action="store_true", help="When true, first col in .info file must be chr:pos (additional pieces allowed)")


        parser.add_argument("--pheno", type=argparse.FileType('r'), help="File containing phenotypes")
        parser.add_argument("--sample-pheno", type=argparse.FileType('r'), help="(Mach) Sample file containing phenotypes")
        parser.add_argument("--mphenos", type=str, default="", help="Column number(s) for phenotype to be analyzed if number of columns > 1")
        parser.add_argument("--pheno-names", type=str, default="", help="Name for phenotype(s) to be analyzed (must be in --pheno file)")
        parser.add_argument("--all-pheno", action="store_true", help="Analyze all columns from the phenotype file")
        #parser.add_argument("--all-pheno", action='store_true', help="Analyze each phenotype")

        parser.add_argument("--covar", type=argparse.FileType('r'), help="File containing covariates")
        parser.add_argument("--sample-covar", type=argparse.FileType('r'), help="(Mach) Sample file containing covariates")
        parser.add_argument("--covar-numbers", type=str, default="", help="Comma-separated list of covariate indices")
        parser.add_argument("--covar-names", type=str, default="", help="Comma-separated list of covariate names")
        parser.add_argument("--sex", action='store_true', help="Use sex from the pedigree file as a covariate")
        parser.add_argument("--missing-phenotype", type=float, default=-9.0, help="Encoding for missing phenotypes")

        parser.add_argument("--maf", type=float, default=0.0, help="Minimum MAF allowed for analysis")
        parser.add_argument("--max-maf", type=float, default=1.0, help="MAX MAF allowed for analysis")
        parser.add_argument("--geno", type=float, default=1.0, help="MAX per-SNP missing for analysis")
        parser.add_argument("--mind", type=float, default=1.0, help="MAX per-person missing")

        parser.add_argument("--verbose", action='store_true', help="Output additional data details")

        parser.set_defaults(all_pheno=False, sex=False, mach_chrpos=False)
        args = parser.parse_args(args)


        # Report version, if requested, and exit
        if args.v:
            print >> sys.stderr, "%s: %s" % (os.path.basename(__file__), __version__)
            sys.exit(0)

        if args.vall:
            print >> sys.stderr, "%s: %s" % (os.path.basename(__file__), __version__)
            print >> sys.stderr, "%s: %s" % (os.path.dirname(libgwas.__file__), libgwas.__version__)
            print >> sys.stderr, "%s: %s" % (os.path.dirname(scipy.__file__), scipy.__version__)
            print >> sys.stderr, "%s: %s" % (os.path.dirname(numpy.__file__), numpy.__version__)
            sys.exit(0)

        ###############################################################################################################
        # Here we deal with the various ways we filter SNPs in and out of anlysis
        # We might handle MACH files differently. We'll default the chromosome
        # to be "NA" which is how those can be returned.
        if args.mach is None or args.mach_chrpos:
            BoundaryCheck.chrom = args.chr
        else:
            if args.chr != -1:
                libgwas.Exit(("Positional based filtering (--chr, --from/--to)" +
                        " only work with mach_chrpos. See manual for details."))
            BoundaryCheck.chrom = "NA"
        snps = args.snps.split(",")
        try:
            b = BoundaryCheck(bp=(args.from_bp, args.to_bp),
                      kb=(args.from_kb, args.to_kb),
                      mb=(args.from_mb, args.to_mb))
        except InvalidBoundarySpec, e:
            print >> sys.stderr, "Invalid boundary spec associated: %s" % (e.malformed_boundary)
            sys.exit(1)
        try:
            s = SnpBoundaryCheck(snps=snps)
        except InvalidBoundarySpec, e:
            print >> sys.stderr, "Invalid SNP boundary defined: %s" % (e.malformed_boundary)
            print >> sys.stderr, "SNPs must be either single or have be a range such as rs123-rs345"
            sys.exit(1)

        if b.valid and s.valid:
            print >> sys.stderr, "Only one type of boundary conditions is permitted. Either use --from-bp, etc. or rs123-rs345. "
            sys.exit(1)

        if len(b.bounds) > 0 and not b.valid:
            if BoundaryCheck.chrom == "NA":
                libgwas.Exit(("Positional based filtering (--chr, --from/--to)" +
                        " only work with mach_chrpos. See manual for details."))


        if s.valid:
            DataParser.boundary = s
        # If b isn't valid, we still want to potentially allow for chr and SNPs, it just won't have
        else:
            b.LoadSNPs(snps)
                                        # any actual boundary listings
            DataParser.boundary = b
        DataParser.boundary.LoadExclusions(snps=args.exclude.split(","))

        ###############################################################################################################
        # Setup the various Dataset filter criteria
        DataParser.min_maf = args.maf
        DataParser.max_maf = args.max_maf
        DataParser.snp_miss_tol = args.geno
        DataParser.ind_miss_tol = args.mind

        DataParser.ind_exclusions = ParseIndList(args.remove)

        PhenoCovar.sex_as_covariate = args.sex

        if args.compressed:
            DataParser.compressed_pedigree = True

        DataParser.has_sex = not args.no_sex
        DataParser.has_parents = not args.no_parents
        DataParser.has_fid = not args.no_fid
        DataParser.has_pheno = not args.no_pheno
        DataParser.has_liability = args.liability

        pheno_covar = PhenoCovar()
        self.verbose=False
        if args.verbose:
            self.verbose = True

        if args.file != None or args.ped or args.map:
            if args.ped and not args.map or args.map  and not args.ped:
                print >> sys.stderr, "When analyzing pedigree data, both .map and .ped must be specified"
                sys.exit(1)
            if args.ped:
                dataset = pedigree_parser.Parser(args.map.name, args.ped.name)
            else:
                dataset = pedigree_parser.Parser("%s.map" % (args.file), "%s.ped" % (args.file))

            dataset.load_mapfile(map3=args.map3)
            dataset.load_genotypes(pheno_covar)
        elif args.tfile != None or args.tped or args.tfam:
            if args.tped and not args.tfam or args.tfam and not args.tped:
                print >> sys.stderr, "When analyzing transposed pedigree data, both .tfam and .tped must be specified"
                sys.exit(1)
            if args.tped:
                dataset = transposed_pedigree_parser.Parser(args.tfam.name, args.tped.name)
            else:
                dataset = transposed_pedigree_parser.Parser("%s.tfam" % (args.tfile), "%s.tped" % (args.tfile))
            dataset.load_tfam(pheno_covar)
            dataset.load_genotypes()
        elif args.bfile != None:
            dataset = bed_parser.Parser("%s.fam" % (args.bfile), "%s.bim" % (args.bfile), "%s.bed" % (args.bfile))
            dataset.load_bim(map3=args.map3)
            dataset.load_fam(pheno_covar)
            dataset.load_genotypes()
        elif args.bed or args.bim or args.fam:
            if (args.bed and not args.fam or not args.bim) or (args.bim and not args.bed or not args.fam) or (args.fam and not args.bed or not args.bim):
                print >> sys.stderr, "When analyzing binary pedigree data, .bed, .bim and .fam files must be provided"
                sys.exit(1)
            dataset = bed_parser.Parser(args.fam, args.bim, args.bed)
            dataset.load_bim(map3=args.map3)
            dataset.load_fam(pheno_covar)
            dataset.load_genotypes()
        elif args.impute:
            DataParser.compressed_pedigree = not args.impute_uncompressed

            if (args.impute_offset > 0 and args.impute_count == -1) or (args.impute_offset == -1 and args.impute_count > 0):
                print >> sys.stderr, "--impute-count and --impute_offset must both > 0 if one is set other than -1.  "
                sys.exit(1)
            if DataParser.snp_miss_tol != 1.0:
                print >> sys.stderr, "--geno does not have any impact on imputed data"
                sys.exit(1)
            if DataParser.ind_miss_tol != 1.0:
                print >> sys.stderr, "--mind does not have any impact on imputed data"
                sys.exit(1)
            impute_parser.SetEncoding(args.impute_encoding)
            impute_parser.Parser.info_ext = args.impute_info_ext
            impute_parser.Parser.info_threshold = args.impute_info_thresh
            libgwas.ExitIf("--impute-fam is required for when processing imputed data", args.impute_fam == None)
            archives, chroms, infos = self.ParseImputeFile(args.impute.name, args.impute_offset, args.impute_count)
            dataset = impute_parser.Parser(args.impute_fam.name, archives, chroms, infos)
            dataset.load_family_details(pheno_covar)
            dataset.load_genotypes()
        elif args.mach:

            DataParser.compressed_pedigree = not args.mach_uncompressed
            if (args.mach_offset > 0 and args.mach_count == -1) or (args.mach_offset == -1 and args.impute_count > 0):
                print >> sys.stderr, "--mach-count and --mach_offset must both be > 0 if one is set other than -1. "
                sys.exit(1)
            if DataParser.snp_miss_tol != 1.0:
                print >> sys.stderr, "--geno does not have any impact on imputed data"
                sys.exit(1)
            if DataParser.ind_miss_tol != 1.0:
                print >> sys.stderr, "--mind does not have any impact on imputed data"
                sys.exit(1)
            if BoundaryCheck.chrom != "NA" and not args.mach_chrpos:
                libgwas.Exit(("Positional based filtering (--chr, --from/--to)" +
                        " only work with mach_chrpos. See manual for details."))
            mach_parser.Parser.chrpos_encoding = args.mach_chrpos
            mach_parser.Parser.info_ext = args.mach_info_ext
            mach_parser.Parser.dosage_ext = args.mach_dose_ext
            mach_parser.Parser.chunk_stride = args.mach_chunk_size
            mach_parser.Parser.min_rsquared = args.mach_min_rsquared
            archives, infos = self.ParseMachFile(args.mach.name, args.mach_offset, args.mach_count)
            dataset = mach_parser.Parser(archives, infos)
            dataset.load_family_details(pheno_covar)
            dataset.load_genotypes()

        else:
            parser.print_usage(sys.stderr)
            print >> sys.stderr, "\nNo data has been specified. Users must specify either pedigree or transposed pedigree to continue"
            sys.exit(1)

        if args.pheno or args.sample_pheno:
            mphenos = []
            if args.mphenos != "":
                mphenos = args.mphenos.split(",")

            nphenos = []
            if args.pheno_names != "":
                nphenos = args.pheno_names.split(",")

            if len(mphenos) + len(nphenos) == 0 and not args.all_pheno:
                libgwas.Exit("You must select one or more phenotypes when ")
            sample_file = False
            pheno_filename = args.pheno
            if args.sample_pheno:
                pheno_filename = args.sample_pheno
                sample_file = True
            pheno_covar.load_phenofile(pheno_filename, mphenos, nphenos, sample_file)

        if args.covar:
            pheno_covar.load_covarfile(args.covar, args.covar_numbers.split(","), args.covar_names.split(","))
        pheno_covar.do_standardize_variables = True
        return dataset, pheno_covar

    def ParseImputeFile(self, filename, offset=-1, count=-1):
        chroms = []
        archives = []
        infos = []

        for line in open(filename):
            words = line.split()

            if len(words) < 2:
                print >> sys.stderr, "The impute file has too few columns! It should have the following information at a minimum:"
                print >> sys.stderr, "chr & imputed_datafile with an optional .info file if the info files aren't named such that"
                print >> sys.stderr, "they are easy for mvtest to find."
                sys.exit(1)

            chroms.append(int(words[0]))
            archives.append(words[1])
            if len(words) > 2:
                infos.append(words[2])
        if offset >= 0 and count > 0:
            offset -= 1
            archives = archives[offset:offset+count]
            chroms = chroms[offset:offset+count]
            if len(infos) > 0:
                infos = infos[offset:offset+count]

        libgwas.ExitIf("The impute file listing appears to be misconfigured. All lines must have the same number of columns", len(infos) != 0 and len(infos) != len(archives))
        return archives, chroms, infos
    def ParseMachFile(self, filename, offset=-1, count=-1):
        archives = []
        infos = []

        for line in open(filename):
            words = line.split()

            if len(words) < 1:
                print >> sys.stderr, "The Mach file has too few columns! It should have the following information at a minimum:"
                print >> sys.stderr, "imputed_datafile with an optional .info file if the info files aren't named such that"
                print >> sys.stderr, "they are easy for mvtest to find."
                sys.exit(1)

            archives.append(words[0])
            if len(words) > 2:
                infos.append(words[1])
        if offset >= 0 and count > 0:
            offset -= 1
            archives = archives[offset:offset+count]
            if len(infos) > 0:
                infos = infos[offset:offset+count]

        libgwas.ExitIf("The mach file listing appears to be misconfigured. All lines must have the same number of columns", len(infos) != 0 and len(infos) != len(archives))
        return archives, infos
    def BuildReportLineIf(self, f, key, doPrint, value="TRUE"):
        if doPrint:
            print >> f, BuildReportLine(key, value)

    def ReportConfiguration(self, args=[], f=sys.stdout, dataset=None):
        """Report on the status of application objects. """
        print >> f, BuildReportLine("MVTEST", __version__)

        print >> f, BuildReportLine("MIN MAF", DataParser.min_maf)
        print >> f, BuildReportLine("MAX MAF", DataParser.max_maf)
        print >> f, BuildReportLine("MISS IND TOL", DataParser.ind_miss_tol)
        print >> f, BuildReportLine("MISS SNP TOL", DataParser.snp_miss_tol)
        print >> f, BuildReportLine("PHENO MISS ENC", PhenoCovar.missing_encoding)
        self.BuildReportLineIf(f, "COMPRESSED PEDIGREE", DataParser.compressed_pedigree)
        self.BuildReportLineIf(f, "SEX AS COV", PhenoCovar.sex_as_covariate)
        self.BuildReportLineIf(f, "NO SEX", not DataParser.has_sex)
        self.BuildReportLineIf(f, "NO PARENTS", not DataParser.has_parents)
        self.BuildReportLineIf(f, "NO FID", not DataParser.has_fid)
        self.BuildReportLineIf(f, "PHENO in PED", DataParser.has_pheno)
        self.BuildReportLineIf(f, "HAS LIABILITY", DataParser.has_liability)
        print >> f, BuildReportLine("MISSING GENO", DataParser.missing_representation)
        if self.verbose:
            print >> f, BuildReportLine("VERBOSE", "TRUE")
        DataParser.boundary.ReportConfiguration(f)

        try:
            index = args.index("MAP3")
            print >> f, BuildReportLine("MAP3", "TRUE")
        except:
            pass

        if dataset:
            dataset.ReportConfiguration(f)

        print >> f, BuildReportLine("SCIPY", scipy.__version__)
        print >> f, BuildReportLine("NUMPY", numpy.__version__)


def main(args=sys.argv[1:], print_cfg=False):
    """Entry point for actual script. """
    try:
        app = MVTestApplication()
        dataset, vars = app.LoadCmdLine(args)

        if print_cfg:
            app.ReportConfiguration(args=args, f=sys.stdout, dataset=dataset)

        printed_header = False

        anl_fn = mv_esteq.RunAnalysis
        for result in anl_fn(dataset, vars):
            if not printed_header:
                result.print_header(verbose=app.verbose)
                printed_header = True
            result.print_result(verbose=app.verbose)

    except ReportableException, e:
        print >> sys.stderr, e.msg


if __name__ == "__main__":
    main(print_cfg=True)
