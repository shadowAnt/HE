# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet

print("\n\n")
print ("=" * 90)
print ("Creating key")
print ("=" * 90)
key = Fernet.generate_key()
print ("Key: " + str(key))

cipher_suite = Fernet(key)

vals = [
[0, 0, 0],
[0, 0, 1],
[0, 1, 0],
[0, 1, 1],
[1, 0, 0],
[1, 0, 1],
[1, 1, 0],
[1, 1, 1]]

S_out = {}
Cout_out = {}

for i in range(len(vals)):
    # initial values
    print( "\n\n")
    print ("=" * 90)
    print ("Initial values")
    print ("=" * 90)
    x = vals[i][0]
    y = vals[i][1]
    cin = vals[i][2]

    print( "x= " + str(x) + ", y= " + str(y) + ", cin= " + str(cin))

# represent the initial values of x, y, cin
# print "  a "+" b "+"cin"
# print " "+"=" * 10
# print('\n'.join([''.join(['{:3}'.format(item) for item in row])
#       for row in vals]))

# print "x=" + str(x)
# print "y=" + str(y)
# print "cin=" +str(cin)

    # logical gates
    print ("\n")
    print( "=" * 90)
    print (" Logical Gates (for reference)")
    print ("=" * 90)
    gate_AND = lambda x, y: x and y
    print ("AND gate with input x=%s, y=%s: " % (x, y) + str(gate_AND(x,y)))

    gate_XOR = lambda x, y: x ^ y
    print ("XOR gate with input x=%s, y=%s: " % (x, y) + str(gate_XOR(x,y)))

    gate_OR = lambda x, y: x or y
    print ("OR gate with input x=%s, y=%s: " % (x, y) + str(gate_OR(x,y)))

    # Mapping the gates to id's
    gates = {0:'XOR', 1:'XOR', 2:'AND', 3:'AND', 4:'OR'}

    # Necessary in order to retrieve the output of the gates
    # that have initial inputs *only*. Then we use their out put
    # to the middle ones that have both initial values and output
    # of other gates. Finally, we get the final output.
    in_gates = [0, 3]
    mid_gates = [1, 2]
    out_gates = [4]

    # Initialization of a dictionary to store the output of each gate
    # *Not really Necessary to initialize it this way*
    results = {0:'', 1:'', 2:'', 3:'', 4:''}

    # We use this function in order to decide which logical operation we will use
    def calculate(g_id, input_1, input_2):
        if gates[g_id] == "XOR":
            gate = lambda input_1, input_2: input_1 ^ input_2
        elif gates[g_id] == "OR":
            gate = lambda input_1, input_2: input_1 or input_2
        elif gates[g_id] == "AND":
            gate = lambda input_1, input_2: input_1 and input_2
        output = gate(input_1,input_2)
        results[g_id] = output
        return output
    # DEBUG
    # print "\nCalculate: " + str(calculate(0, x, y))
    # DEBUG


    out_in = []
    def calc_in_gates(*in_gates):
        #print x,y
        # print in_gates
        for i in in_gates:
            # print i
            out_in.append(str(calculate(i,x,y)))
        return out_in

    out_mid = []
    def calc_mid_gates(*mid_gates):
        for i in mid_gates:
            out_mid.append(str(calculate(i, results[0], cin)))
        return out_mid

    out_out = []
    def calc_out_gates(*out_gates):
        for i in out_gates:
            # print i
            out_out.append(str(calculate(i,results[2],results[3])))
            # out = calculate(i,results[2],results[3])
        return out_out

    # Needs more detailed reference
    print( "\n")
    print( "Calculate input gates: " + str(calc_in_gates(*in_gates)))
    print ("Calculate mid gates: " + str(calc_mid_gates(*mid_gates)))
    print ("Calculate out gates: " + str(calc_out_gates(*out_gates)))

    # Not sure what I wanted to do here :-)
    # def calc_circuit(**gates):
    #     print "\n"
    #     for i in gates.keys():
    #         print i, gates[i]
    # print "\nCalculate circuit: " + str(calc_circuit(**{str(k): v for k, v in gates.items()}))


    # Printing the outputs of the gates - Important! (for each round of x, y, cin values)
    def print_output(**results):
        print( "\nResults: ") #+ str(results)
        print( "Gate id"+"     "+"Output")
        for i in results:
            print ("   " + str(i) + "    -->    " + str(results[i]))

    print( print_output(**{str(k): v for k,v in results.items()}))

    def get_S_Cout():
        S_out['S'+str(i)] = results[1]
        Cout_out['Cout'+str(i)] = results[4]

    get_S_Cout()
S_out
Cout_out
    # #Print truth table - Not sure yet how to construct it
    # def print_truth_table(gate, input_1, input_2):
    #     # print " x " + " y " + "cin" + " " + "|" + " " + "Cout" + " S "
    #     # print "=" * 19
    #     # for i in range(len())
    #     # print truths.Truths(['a', 'b', 'cin'],['a or b'])
    #     print " x " + " y " + " | " + gate
    #     print "=" * 6 + "=|=" + "=" * 3
    #     print " 0 " + " 0 " + " | " + " R "
    #     print " 0 " + " 1 " + " | " + " R "
    #     print " 1 " + " 0 " + " | " + " R "
    #     print " 1 " + " 1 " + " | " + " R "
    # print_truth_table(gates[0], x, y)






#
# # int to byte
# print "\n\n"
# print "=" * 90
# print " Converting int to byte"
# print "=" * 90
# enc_x = bytes(x)
# print "Encoded to byte x: " + enc_x
#
# enc_y = bytes(y)
# print "Encoded to byte y: " + enc_y
#
# # encryption
# print "\n\n"
# print "=" * 90
# print "Encrypting"
# print "=" * 90
# encr_x = cipher_suite.encrypt(enc_x)
# print "Encrypted x: " + encr_x
#
# encr_y = cipher_suite.encrypt(enc_y)
# print "Encrypted y: " + encr_y
#
# # DEBUG
# # decryption
# print "\n\n"
# print "=" * 90
# print "Decrypting - DEBUG"
# print "=" * 90
#
# decr_x = cipher_suite.decrypt(encr_x)
# print "Decrypted x: " + decr_x
#
# decr_y = cipher_suite.decrypt(encr_y)
# print "Decrypted y: " + decr_y