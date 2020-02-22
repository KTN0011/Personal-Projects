#__
#                                                            
# Converts Input Phrase from string to Hexadecimal to Binary 
#__
 
#  String Input to Hexadecimal Conversion
print('Please enter your Phrase: ')
phrase = input()
hex_out = phrase.encode().hex()
print('\n')
print(hex_out)
 
#  Hexadecimal to Binary Conversion
binary_out = bin(int(hex_out, 16))[2:]
print('\n')
print(binary_out)
#  Append 8 '0s' to the front of the Binary String
binary_out = '00000000' + binary_out
print('\n')
print(binary_out)
 
#  Decodes Hexadecimal String to ASCII representation
output_1 = bytes.fromhex(hex_out).decode()
print('\n')
print(output_1)



input = ("1","0","0","1","1")
def v_xor(bit0,bit1):
    if(bit0==bit1):
        return "0"
    else:
        return "1"
def viterbi_encoder(input):
    #shift register encoder
    s_reg = ["0","0","0"]
    obs = []
    for t in range (0,len(input)):
        #shifting the bits to right
        s_reg[2]=s_reg[1]
        s_reg[1]=s_reg[0]
        #inserting input
        s_reg[0]= input[t]
        state = s_reg[0]+ s_reg[1]
        obs.append([])
        #encoded bits
        obs[t] = v_xor(v_xor(s_reg[0],s_reg[1]),s_reg[2])+\
            v_xor(s_reg[0],s_reg[2])
        print (s_reg,state)
    print (obs)


obs = ("11","10","11","11","01","01","11")
start_metric = {'zero':0,'one': 0, 'two': 0,'three':0}
state_machine = {
    #current state, possible branches, branch information
    'zero': {'b1': {'out_b':"11",'prev_st': 'one','input_b':0},
             'b2': {'out_b':"00",'prev_st': 'zero','input_b':0}},
    'one': {'b1': {'out_b': "01", 'prev_st': 'three', 'input_b': 0},
             'b2': {'out_b': "10", 'prev_st': 'two', 'input_b': 0}},
    'two': {'b1': {'out_b': "11", 'prev_st': 'zero', 'input_b': 1},
             'b2': {'out_b': "00", 'prev_st': 'one', 'input_b': 1}},
    'three': {'b1': {'out_b': "10", 'prev_st': 'three', 'input_b': 1},
             'b2': {'out_b': "01", 'prev_st': 'two', 'input_b': 1}},
 
}
 
def bits_diff_num(num_1,num_2):
    count=0;
    for i in range(0,len(num_1),1):
        if num_1[i]!=num_2[i]:
            count=count+1
    return count
 
def viterbi(obs, start_metric, state_machine):
    #Trellis structure
    V = [{}]
    for st in state_machine:
        # Calculating the probability of both initial possibilities for the first observation
        V[0][st] = {"metric": start_metric[st]}
    #for t&amp;amp;amp;amp;amp;amp;amp;amp;gt;0
    for t in range(1, len(obs)+1):
        V.append({})
        for st in state_machine:
            #Check for smallest bit difference from possible previous paths, adding with previous metric
            prev_st = state_machine[st]['b1']['prev_st']
            first_b_metric = V[(t-1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b1']['out_b'], obs[t - 1])
            prev_st = state_machine[st]['b2']['prev_st']
            second_b_metric = V[(t - 1)][prev_st]["metric"] + bits_diff_num(state_machine[st]['b2']['out_b'], obs[t - 1])
            #print(state_machine[st]['b1']['out_b'],obs[t - 1],t)
            if first_b_metric > second_b_metric:
                V[t][st] = {"metric" : second_b_metric,"branch":'b2'}
            else:
                V[t][st] = {"metric": first_b_metric, "branch": 'b1'}
 
    #print trellis nodes metric:
    for st in state_machine:
        for t in range(0,len(V)):
            print(V[t][st]["metric"], end=" "),
        print("")
    print("")
 
    smaller = min(V[t][st]["metric"] for st in state_machine)
    #traceback the path on smaller metric on last trellis column
    for st in state_machine:
        if V[len(obs)-1][st]["metric"] == smaller:
            source_state = st
            for t in range(len(obs),0,-1):
                branch = V[t][source_state]["branch"]
                print(state_machine[source_state][branch]['input_b']),
                source_state = state_machine[source_state][branch]['prev_st']
            print (source_state+"\n")
    print("Finish")
 
viterbi(obs,
        start_metric,
        state_machine)