import io, os, csv, sys
import argparse

from predictor.model import computePredictedProfile, readTheta, setFeaturesDir, setReadsDir
from predictor.features import calculateFeaturesForGenIndelFile, readFeaturesData
from predictor.predict import predictMutationsBulk, predictMutationsSingle, predictMutationsBulkInFrame

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Scripts for processing and predicting CRISPR/Cas9-generated mutations")
    parser.add_argument("-s", "--single", help="Run single gRNA prediction", action="store_true")
    parser.add_argument("-t", "--target", help="23bp target sequence to use when running single gRNA prediction")
    parser.add_argument("-p", "--pam", help="PAM index (0 based) to use when running single gRNA prediction")
    parser.add_argument("-b", "--batch", help="Run batch gRNA prediction", action="store_true")
    parser.add_argument("-i", "--input", help="Input file for batch gRNA prediction")
    parser.add_argument("-o", "--output", help="Output file prefix")
    parser.add_argument("--inFrame", help="Output only in frame percentage when using batch mode", action="store_true")
    args = parser.parse_args()

    if args.batch: #Batch mode
    
        if args.input == None or args.output == None:
            parser.error("--batch requires --input <batch_filename> and --output <output_file_prefix>")

        batch_file = args.input
        output_prefix = args.output
    
        if not os.path.isfile(batch_file):
            raise Exception('Count not find batch file ' + batch_file)

        if args.inFrame == None:
            predictMutationsBulk(batch_file, output_prefix)
        else:
            predictMutationsBulkInFrame(batch_file, output_prefix)

    elif args.single:    #Single mode

        if args.target == None or args.pam == None or args.output == None:
            parser.error("--single requires --target <target DNA sequence> and --pam <PAM index (0 based)> and --output <output_file_prefix>")


        target_seq = args.target
        if sum([x not in 'ATGC' for x in target_seq]) > 0:
            raise Exception('Invalid target sequence, expecting string containing only A,T,G,C:\n%s' % target_seq)
        try:
            pam_idx = eval(args.pam)
        except:
            raise('Could not parse PAM index, expected an integer %s' % pam_idx)
        output_prefix = args.output
            
        predictMutationsSingle(target_seq, pam_idx, output_prefix)
    
    else:
        err_str = 'FORECasT: Invalid inputs. Usage:\n\nSingle gRNA: python FORECasT.py <guide_sequence> <PAM index (0 based)> <output_prefix>'
        err_str += '\n\nBatch gRNA: python FORECasT.py <batch_filename> <output_prefix>\n'
        raise Exception(err_str)
    
