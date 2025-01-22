'''

IFN646 Biomedical Data Science,
Queensland University of Technology

Portfolio 3 Checker

- This script is designed to validate the structure of the objects returned
    by each of the functions that we will test.
    
- Requirements:
    o Python version 3.6 or above
    o This script and your solution exist in the same directory

- During marking, three functions will be ran against your allocated datasets:
    1. TaskA(..)
    2. TaskB(..)
    3. TaskC(..)

- How does this work?
    o There is a line of code below which is intended to import your solution.
      If you have followed the instructions correctly, which means, you have
        renamed the portfolio3.py script to be <your-student-id>.py
        then you need to update this line with your student ID.
    o If we find structural errors, we will let you know.
    
- What does this script not do?
    o This script does not report that your answers are correct or incorrect.
    o We want to make sure that, at least, you have correctly structured
        the output produced by the three functions.
        
- What now?
    o Update the import line, found below. Do not modify any other code.


'''

######################################################
##         Update this line with the name           ##
##             of your solution file.               ##
##            (this should be your ID)              ##
##                                                  ##
SOLUTION_FILE_NAME = r"n11371200"                ##
##                                                  ##
##                                                  ##
##            Do not modify below here!             ##
######################################################

def runChecks(moduleToImport):
    FUNCS = ["TaskA", "TaskB", "TaskC"]
    FUNC_ARGS = {
        "TaskA" : ['F_GENOME'],
        "TaskB" : ['F_GENOME', 'F_GUIDES'],
        "TaskC" : ['F_GENOME', 'F_GUIDES'],
    }

    FUNCS_TO_CHECK = []
    FUNCS_TO_MARK = []


    ### Try importing the module
    try:
        import importlib
        importlib.invalidate_caches()
        pf3 = importlib.import_module(moduleToImport)
    except BaseException as err:
        print(f"Failed to import your solution.")
        print(f"You specified: {moduleToImport}")
        print(f"Error: {err}")
        print(f"Exiting.")
        exit()
        
        

    ### Check that the functions still exist
    import inspect
    for i in range(len(FUNCS)):
        func = FUNCS[i]
        if func not in pf3.__dict__.keys():
            print(f"You are missing {func} in your solution")
        else:
            FUNCS_TO_CHECK.append(func)


    ### Check that the functions contain the correct arguments
    for func in FUNCS_TO_CHECK:
        temp = eval(f"pf3.{func}")
        funcArgs = [x for x in inspect.signature(temp).parameters]

        if len(funcArgs) != len(FUNC_ARGS[func]):
            print(f"{func} should contain {len(FUNC_ARGS[func])} arguments but yours contains {len(funcArgs)}.\n\tThe arguments should be (in this order):")
            for arg in FUNC_ARGS[func]:
                print(f"\t\t{arg}")
                
        
    ### Check the structure of the output
    import tempfile
    tempGenome = tempfile.NamedTemporaryFile('w', delete=False)
    with open(tempGenome.name, 'w+') as fpGenome:
        fpGenome.write(""">A genome...
AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGCTTCTGAACTG
GTTACCTGCCGTGAGTAAATTAAAATTTTATTGACTTAGGTCACTAAATACTTTAACCAATATAGGCATAGCGCACAGAC
AGATAAAAATTACAGAGTACACAACATCCATGAAACGCATTAGCACCACCATTACCACCACCATCACCATTACCACAGGT
AACGGTGCGGGCTGACGCGTACAGGAAACACAGAAAAAAGCCCGCACCTGACAGTGCGGGCTTTTTTTTTCGACCAAAGG
TAACGAGGTAACAACCATGCGAGTGTTGAAGTTCGGCGGTACATCAGTGGCAAATGCAGAACGTTTTCTGCGTGTTGCCG
ATATTCTGGAAAGCAATGCCAGGCAGGGGCAGGTGGCCACCGTCCTCTCTGCCCCCGCCAAAATCACCAACCACCTGGTG
GCGATGATTGAAAAAACCATTAGCGGCCAGGATGCTTTACCCAATATCAGCGATGCCGAACGTATTTTTGCCGAACTTTT
GACGGGACTCGCCGCCGCCCAGCCGGGGTTCCCGCTGGCGCAATTGAAAACTTTCGTCGATCAGGAATTTGCCCAAATAA
AACATGTCCTGCATGGCATTAGTTTGTTGGGGCAGTGCCCGGATAGCATCAACGCTGCGCTGATTTGCCGTGGCGAGAAA
ATGTCGATCGCCATTATGGCCGGCGTATTAGAAGCGCGCGGTCACAACGTTACTGTTATCGATCCGGTCGAAAAACTGCT
GGCAGTGGGGCATTACCTCGAATCTACCGTCGATATTGCTGAGTCCACCCGCCGTATTGCGGCAAGCCGCATTCCGGCTG
ATCACATGGTGCTGATGGCAGGTTTCACCGCCGGTAATGAAAAAGGCGAACTGGTGGTGCTTGGACGCAACGGTTCCGAC
TACTCTGCTGCGGTGCTGGCTGCCTGTTTACGCGCCGATTGTTGCGAGATTTGGACGGACGTTGACGGGGTCTATACCTG
CGACCCGCGTCAGGTGCCCGATGCGAGGTTGTTGAAGTCGATGTCCTACCAGGAAGCGATGGAGCTTTCCTACTTCGGCG
CTAAAGTTCTTCACCCCCGCACCATTACCCCCATCGCCCAGTTCCAGATCCCTTGCCTGATTAAAAATACCGGAAATCCT
""")
    
    tempGuides = tempfile.NamedTemporaryFile('w', delete=False)
    with open(tempGuides.name, 'w+') as fpGuides:
        fpGuides.write("""TATGCAGAACAATGAGCAGACGG
GCGATAAGCGTGAGCAGTGACGG
CAGTCTGGAAGCCCGTGCGCTGG
AATAATCCCTACCGGCGCAGAGG
GCCAGTGCCTGTGTGCGTTGCGG
ACTGCATCAGGCGTGGCAGGCGG
ATTGCGCGCACCCATAACGCGGG
AATTAGTCAAAAAGAAACCCCGG
GCCAGTGCTTACGAACGTCAGGG
GTGGGGCTACTTCCTCCATCAGG
""")

    passed = True

    # Tedious but we need to do it this way...
    if 'TaskA' in FUNCS_TO_CHECK:    
        passed = checkTaskA(pf3, tempGenome.name)
        if passed:
            FUNCS_TO_MARK.append('TaskA')
    print("\n")        
    if 'TaskB' in FUNCS_TO_CHECK:    
        passed = checkTaskB(pf3, tempGenome.name, tempGuides.name)
        if passed:
            FUNCS_TO_MARK.append('TaskB')
    print("\n")    
    if 'TaskC' in FUNCS_TO_CHECK:    
        passed = checkTaskC(pf3, tempGenome.name, tempGuides.name)
        if passed:
            FUNCS_TO_MARK.append('TaskC')
 

    if not passed:
        print("\n")   
        print("Something went wrong. Please read the warnings, above, carefully.")
        
    print("\n")    
    print('Goodbye.')  
    return FUNCS_TO_MARK
    
def checkTaskA(modPf3, fpGenome):
    passed = True
    print("Checking TaskA")
    
    updatedGlobalVariables = False
    try:
        offtargets = modPf3.TaskA(fpGenome)
    except IOError as e:
        print(f"\t- There was an IO error: {e}")
        print("\t- Trying again but with updating global variables")
        modPf3.INPUT_GENOME = fpGenome
        offtargets = modPf3.TaskA("")
        updatedGlobalVariables = True
    except Exception as e:
        print("\t! Something went wrong with running TaskA.")
        print(f"\t{e}")
        return False

    if updatedGlobalVariables:
        print("\t! You are not using the function argument correctly.")
        print("\t\t When reading in the file, do not use INPUT_GENOME,")
        print("\t\t but instead, use the function argument, F_GENOME.")
        passed = False
    
    if isinstance(offtargets, list):
        print(f"\t- Returned a list of size {len(offtargets)}")
        contentsFailed = False
        for offtarget in offtargets:
            contentsFailed |= not isinstance(offtarget, str)
         
        if contentsFailed:
            passed = False
            print("\t! Your list should only contain strings (off-targets). It contains something else.")
            
    else:
        passed = False
        print("\t! The object that TaskA returned is not a list.")
    
    if passed:
        print("\t- Passed all checks.")
    print("\t- Finished checking TaskA.")
    return passed

def checkTaskB(modPf3, fpGenome, fpGuides):
    passed = True
    print("Checking TaskB")
    
    updatedGlobalVariables = False
    try:
        mismatchesLists = modPf3.TaskB(fpGenome, fpGuides)
    except IOError as e:
        print(f"\t- There was an IO error: {e}")
        print("\t- Trying again but with updating global variables")
        modPf3.INPUT_GENOME = fpGenome
        modPf3.INPUT_GUIDES = fpGuides
        offtargets = modPf3.TaskB("", "")
        updatedGlobalVariables = True
    except Exception as e:
        print("\t! Something went wrong with running TaskB.")
        print(f"\t{e}")
        return False

    if updatedGlobalVariables:
        print("\t! You are not using the function arguments correctly.")
        print("\t\t When reading in the files, do not use INPUT_GENOME,")
        print("\t\t or INPUT_GUIDES, but instead, use the function")
        print("\t\t arguments F_GENOME and F_GENOME.")
        passed = False
     
    if isinstance(mismatchesLists, list):
        print(f"\t- Returned a list containing {len(mismatchesLists)} object(s).")
        i = 0
        for mismatchesList in mismatchesLists:
            if not isinstance(mismatchesList, list):
                print(f"\t! Object {i} in the list returned by TaskB is not a list.")
                passed = False
                
            else:
                if len(mismatchesList) != 6:
                    print(f"\t! List {i}: incorrect size (it contains {len(mismatchesList)} object(s), it should contain 6).")
                    passed = False
                else:
                    if not isinstance(mismatchesList[0], str):
                        print(f"\t! List {i}: the first object is not a string. This should be a candidate guide sequence.")
                        passed = False
                    if not all([isinstance(mismatchesList[x], (int, float)) for x in range(1, 6)]):
                        print(f"\t! List {i}: the objects in positions 1-5 (0-index) should be numbers (one for each mismatches count).")
                        passed = False
            i += 1
            
    else:
        print("\t! The object that TaskB returned is not a list.")
        passed = False
        
    if passed:
        print("\t- Passed all checks.")
    print("\t- Finished checking TaskB.")
    return passed
    
def checkTaskC(modPf3, fpGenome, fpGuides):
    passed = True
    print("Checking TaskC")
    
    updatedGlobalVariables = False
    try:
        scoresLists = modPf3.TaskC(fpGenome, fpGuides)
    except IOError as e:
        print(f"\t- There was an IO error: {e}")
        print("\t- Trying again but with updating global variables")
        modPf3.INPUT_GENOME = fpGenome
        modPf3.INPUT_GUIDES = fpGuides
        offtargets = modPf3.TaskC("", "")
        updatedGlobalVariables = True
    except Exception as e:
        print("\t! Something went wrong with running TaskC")
        print(f"\t{e}")
        return False

    if updatedGlobalVariables:
        print("\t! You are not using the function arguments correctly.")
        print("\t\t When reading in the files, do not use INPUT_GENOME,")
        print("\t\t or INPUT_GUIDES, but instead, use the function")
        print("\t\t arguments F_GENOME and F_GENOME.")
        passed = False

    if isinstance(scoresLists, list):
        print(f"\t- Returned a list containing {len(scoresLists)} object(s).")
        i = 0
        for scoresList in scoresLists:
            if not isinstance(scoresList, list):
                print(f"\t! Object {i} in the list returned by TaskC is not a list.")
                passed = False
                
            else:
                if len(scoresList) != 2:
                    print(f"\t! List {i}: incorrect size (it contains {len(scoresList)} object(s), it should contain 2).")
                    passed = False
                else:
                    if not isinstance(scoresList[0], str):
                        print(f"\t! List {i}: the first object is not a string. This should be a candidate guide sequence.")
                        passed = False
                    if not isinstance(scoresList[1], (int, float)):
                        print(f"\t! List {i}: the second object is not a number. This should be the off-target score.")
                        passed = False
            i += 1
            
    else:
        print("\t! The object that TaskC returned is not a list.")
        passed = False
    
    if passed:
        print("\t- Passed all checks.")
    print("\t- Finished checking TaskC.")
    return passed
    
    
if __name__ == '__main__':
    print("\n-- IFN646 Portfolio 3 Checker (v3) --\n")
    
    if SOLUTION_FILE_NAME == 'TYPE_YOUR_FILE_NAME_HERE':
        print("test")
        print("You need to update the variable SOLUTION_FILE_NAME within this script.\n")
        print("Exiting.")
        exit()
        
    runChecks(SOLUTION_FILE_NAME)
    