#!/usr/bin/python

import util

class MException(Exception):
    def __init__(self, msg):
        util.print_status(util.TASK_ERROR)
        super(MException, self).__init__(msg)


class TranscriptFileNotExistException(MException):
    def __init__(self):
        super(TranscriptFileNotExistException, self).__init__(util.REPORT + "transcript file is missing | data/protein_refseq.fasta")


class ProteinFileNotExistException(MException):

    def __init__(self):
        super(ProteinFileNotExistException, self).__init__(util.REPORT + "protein file is missing | data/transcript_refseq.fasta")


class FileHasBeenModified(MException):
    def __init__(self, msg):
        super(FileHasBeenModified, self).__init__(msg)


class OptNotHandledException(MException):

    def __init__(self, msg):
        super(OptNotHandledException, self).__init__(util.REPORT + msg)


class InputMissingException(MException):

    def __init__(self):
        super(InputMissingException, self).__init__(util.REPORT + "input is missing" + "\n" + util.GENERAL_USAGE)


class InputFileNotExistException(MException):

    def __init__(self, input):
        super(InputFileNotExistException, self).__init__(util.REPORT + "input file does not exist | " + input)


class TooMuchArgumentsException(MException):

    def __init__(self, args):
        super(TooMuchArgumentsException, self).__init__(util.REPORT + "too much arguments | " + ", ".join(args) + "\n" + util.GENERAL_USAGE)

class AllelePredictionException(MException):

    def __init__(self, input):
        super(InputFileNotExistException, self).__init__(util.REPORT + "Process not concluded ")


class InvalidPeptideLengthException(MException):

    def __init__(self):
        super(InvalidPeptideLengthException, self).__init__(util.REPORT + "invalid peptide length")


class PeptideLengthMissingException(MException):

    def __init__(self):
        super(PeptideLengthMissingException, self).__init__(util.REPORT + "peptide length is missing")


class InvalidMethodException(MException):
    def __init__(self, p_class):
    	if p_class == 1:
            super(InvalidMethodException, self).__init__(util.REPORT + "invalid method. " + str(util.PREDICT_METHODS_CLASS_I))
        else:
            super(InvalidMethodException, self).__init__(util.REPORT + "invalid method. " + str(util.PREDICT_METHODS_CLASS_II))


class VCFWrongFormat(MException):

    def __init__(self, msg):
        super(VCFWrongFormat, self).__init__(msg)


class InvalidFilterException(MException):
    def __init__(self):
        super(InvalidFilterException, self).__init__(util.REPORT + "invalid filter. " + str(util.IEDB_RECOMMENDED_FILTER_LIST))


class FilterMissingException(MException):
    def __init__(self):
        super(FilterMissingException, self).__init__(util.REPORT + "filter is missing")


class InvalidFilterCutOffException(MException):

    def __init__(self):
        super(InvalidFilterCutOffException, self).__init__(util.REPORT + "invalid filter cut-off")


class FilterCutOffMissingException(MException):
    def __init__(self):
        super(FilterCutOffMissingException, self).__init__(util.REPORT + "filter cut-off is missing")


class NoMutatedFileWasFoundException(MException):
    def __init__(self):
        super(NoMutatedFileWasFoundException, self).__init__(util.REPORT + "no mutated file was found")


class NoBindingPredictionFileWasFoundException(MException):
    def __init__(self):
        super(NoBindingPredictionFileWasFoundException, self).__init__(util.REPORT + "no binding prediction file was found")


class BindingPredictionException(MException):
    def __init__(self, msg):
        super(BindingPredictionException, self).__init__(util.REPORT + msg)


class InvalidCoreNumberException(MException):
    def __init__(self):
        super(InvalidCoreNumberException, self).__init__(util.REPORT + "invalid core number")
        

class InvalidClassException(MException):
    def __init__(self):
        super(InvalidClassException, self).__init__(util.REPORT + "invalid class")


class ClassMissingException(MException):
    def __init__(self):
        super(ClassMissingException, self).__init__(util.REPORT + "class definition is missing")


class InputExpressionDataWrongFormat(MException):
     def __init__(self):
        super(InputExpressionDataWrongFormat, self).__init__(util.REPORT + "invalid expression input file")


class ExpressionInputIsEmpty(MException):
    def __init__(self):
        super(ExpressionInputIsEmpty, self).__init__(util.REPORT + "directory " + inputExpression + "is empty ")


class QuantifyingExpressionException(MException):
    def __init__(self, msg):
        super(QuantifyingExpressionException, self).__init__(util.REPORT + msg)

class InvalidFunction(MException):
    def __init__(self):
        super(InvalidFunction, self).__init__(util.REPORT + "invalid function. " + str(util.FUNCTIONS))
        
class PreProcessingVariantCallingException(MException):
    def __init__(self):
        super(PreProcessingVariantCallingException, self).__init__(util.REPORT + "BAM processing error")
        
        
class VCFAnnotationFailed(MException):
    def __init__(self):
        super(VCFAnnotationFailed, self).__init__(util.REPORT + "Annotation incomplete")

