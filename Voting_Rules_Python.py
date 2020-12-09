#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np

pairwise_graph = open("ED-00009-00000001.pwg", "r")
pairwise_graph_lines = pairwise_graph.readlines()

voting_profile = open("ED-00009-00000001.soc", "r")
voting_profile_lines = voting_profile.readlines()

def check_for_condorcet_winner(pairwise_graph_lines):
    start_point = int(pairwise_graph_lines[0]) + 2
    candidates = np.zeros((int(pairwise_graph_lines[0]), int(pairwise_graph_lines[0])))
    counter = 0
    for line in pairwise_graph_lines[1:]:
        if counter < start_point - 1:
            if counter < start_point - 2:
                counter = counter + 1
            else:
                total_number_voters, total_rankings, unique_rankings = line.split(",")
                total_number_voters = int(total_number_voters)
                counter = counter + 1
                continue
        else:
            weight, source, destination = line.split(",")
            candidates[int(source) - 1][int(destination) - 1] = total_number_voters
    #print(candidates)
    condorcet_winner_l = [True] * len(candidates)
    for i in range(0, len(candidates)):
        for j in range(0, len(candidates)):
            if i == j:
                continue
            else:
                if candidates[i][j] < candidates[j][i]:
                    condorcet_winner_l[i] = False
                    
    #print(condorcet_winner_l)
    condorcet_winner = None
    for i in range(0, len(condorcet_winner_l)):
        if condorcet_winner_l[i] == True:
            condorcet_winner = i + 1
            
    return candidates, condorcet_winner


candidates, condorcet_winner = check_for_condorcet_winner(pairwise_graph_lines)

print("Alternative", condorcet_winner, "is a Condorcet winner")

# 1. Plurality



start_point = int(voting_profile_lines[0]) + 2

points_plurality = [0] * (len(candidates))

counter = 0
for line in voting_profile_lines[1:]:
    if counter < start_point - 1:
        if counter < start_point - 2:
            counter = counter + 1
        else:
            total_number_voters, total_rankings, unique_rankings = line.split(",")
            total_number_voters = int(total_number_voters)
            counter = counter + 1
            continue
    else:
        c = [None] * int(voting_profile_lines[0])
        line_list = line.split(",")
        num_of_votes = line_list[0]
        c = []
        for i in range(1, len(line_list)):
            c.append(int(line_list[i]))
        first_place = int(c[1])
        if first_place == condorcet_winner:
            first_place = int(c[2])
        points_plurality[int(first_place) - 1] = points_plurality[int(first_place) - 1] + int(num_of_votes)

winner_plurality = 0
for i in range(1, len(points_plurality)):
    if points_plurality[i] > points_plurality[winner_plurality]:
        winner_plurality = i

#breaking ties lexicographic
for i in range(0, len(points_plurality)):
    if points_plurality[i] == points_plurality[winner_plurality]:
        if i > winner_plurality:
            winner_plurality = i
        
        
        
winner_plurality = winner_plurality + 1
print("Plurality winner: Course", winner_plurality)

# 2. Borda

points_borda = [0] * (len(candidates))

counter = 0
for line in voting_profile_lines[1:]:
        if counter < start_point - 1:
            if counter < start_point - 2:
                counter = counter + 1
            else:
                total_number_voters, total_rankings, unique_rankings = line.split(",")
                total_number_voters = int(total_number_voters)
                counter = counter + 1
                continue
        else:
            c = [None] * int(voting_profile_lines[0])
            line_list = line.split(",")
            num_of_votes = line_list[0]
            c = []
            for i in range(1, len(line_list)):
                c.append(int(line_list[i]))
            points = int(voting_profile_lines[0]) - 1
            for i in range(0, len(c)):
                if int(c[i]) == condorcet_winner:
                    points = points - 1
                    continue
                else:
                    points_borda[int(c[i]) - 1] = points_borda[int(c[i]) - 1] + points
                    points = points - 1
                    
winner_borda = 0
for i in range(1, len(points_borda)):
    if points_borda[i] > points_borda[winner_borda]:
        winner_borda = i
        
#breaking ties lexicographic
for i in range(0, len(points_borda)):
    if points_borda[i] == points_borda[winner_borda]:
        if i > winner_borda:
            winner_borda = i
            
winner_borda = winner_borda + 1
print("Borda winner: Course", winner_borda)



# 3. Nanson

winner_Nanson = None
list_out = []
list_out.append(condorcet_winner)
while (winner_Nanson == None):
    points_Nanson = [0] * (len(candidates))
    counter = 0
    for line in voting_profile_lines[1:]:
        if counter < start_point - 1:
            if counter < start_point - 2:
                counter = counter + 1
            else:
                total_number_voters, total_rankings, unique_rankings = line.split(",")
                total_number_voters = int(total_number_voters)
                counter = counter + 1
                continue
        else:
            c = [None] * int(voting_profile_lines[0])
            line_list = line.split(",")
            num_of_votes = line_list[0]
            c = []
            for i in range(1, len(line_list)):
                c.append(int(line_list[i]))
            points = int(voting_profile_lines[0])-1-len(list_out)
            for i in range(0, len(c)):
                if int(c[i]) in list_out:
                    continue
                else:
                    points_Nanson[int(c[i]) - 1] = points_Nanson[int(c[i]) - 1] + points
                    points = points - 1
                    
    loser_Nanson = None
    if (len(list_out) == int(voting_profile_lines[0]) - 1):
        for i in range(0, len(candidates)):
            if (i + 1) in list_out:
                continue
            else:
                winner_Nanson = i + 1
    else:
        sum_borda = 0
        num_of_left_c = int(voting_profile_lines[0]) - len(list_out)
        for i in range(0, len(points_Nanson)):
            sum_borda = sum_borda + points_Nanson[i]
        avg_borda = sum_borda / num_of_left_c
        all_equal_to_avg = True
        for i in range(0, len(points_Nanson)):
            if points_Nanson[i] != avg_borda:
                all_equal_to_avg = False
                break
        #breaking ties lexicographic
        if all_equal_to_avg == True:
            winner_Nanson = 0
            for i in range(1, len(points_Nanson)):
                if points_Nanson[i] == avg_borda:
                    if i > winner_Nanson:
                        winner_Nanson = i
        else:
            for i in range(0, len(points_Nanson)):
                if (i + 1) in list_out:
                    continue
                else:
                    if points_Nanson[i] < avg_borda:
                        loser_Nanson = i + 1
                        list_out.append(loser_Nanson)
        
        
print("Nanson winner: Course", winner_Nanson)



# 4. Single transferable vote


winner_STV = None
list_out = []
list_out.append(condorcet_winner)
while (winner_STV == None):
    points_STV = [0] * (len(candidates))
    counter = 0
    for line in voting_profile_lines[1:]:
        if counter < start_point - 1:
            if counter < start_point - 2:
                counter = counter + 1
            else:
                total_number_voters, total_rankings, unique_rankings = line.split(",")
                total_number_voters = int(total_number_voters)
                counter = counter + 1
                continue
        else:
            c = [None] * int(voting_profile_lines[0])
            line_list = line.split(",")
            num_of_votes = line_list[0]
            c = []
            for i in range(1, len(line_list)):
                c.append(int(line_list[i]))
            first_place = int(c[0])
            for i in range(1, len(c)):
                if first_place in list_out:
                    first_place = int(c[i])
            else:
                points_STV[int(first_place) - 1] = points_STV[int(first_place) - 1] + int(num_of_votes)
                
    loser_STV = 0
    if (len(list_out) == int(voting_profile_lines[0]) - 1):
        for i in range(0, len(points_STV)):
            if points_STV[i] != 0:
                winner_STV = i + 1
    else:      
        for i in range(1, len(points_STV)):
            if (loser_STV + 1) in list_out:
                loser_STV = i
            if (i + 1) in list_out:
                continue
            elif points_STV[i] < points_STV[loser_STV]:
                loser_STV = i
        loser_STV = loser_STV + 1
        list_out.append(loser_STV)
    
print("STV winner: Course", winner_STV)



# 5. Copeland

candidates_copeland = np.zeros((int(voting_profile_lines[0]), int(voting_profile_lines[0])))

counter = 0
for line in voting_profile_lines[1:]:
    if counter < start_point - 1:
        if counter < start_point - 2:
            counter = counter + 1
        else:
            total_number_voters, total_rankings, unique_rankings = line.split(",")
            total_number_voters = int(total_number_voters)
            counter = counter + 1
            continue
    else:
        c = [None] * int(voting_profile_lines[0])
        line_list = line.split(",")
        num_of_votes = line_list[0]
        c = []
        for i in range(1, len(line_list)):
            c.append(int(line_list[i]))
        first_place = int(c[0])
        if first_place == condorcet_winner:
            c.remove(c[0])
        for i in range(0, len(c)):
            for j in range(i + 1, len(c)):
                candidates_copeland[int(c[i]) - 1][int(c[j]) - 1] = candidates_copeland[int(c[i]) - 1][int(c[j]) - 1] + int(num_of_votes)

out_degree = [0] * (len(candidates_copeland))

for i in range(0, len(candidates_copeland)):
    for j in range(0, len(candidates_copeland)):
        if i == j:
            continue
        elif (i + 1) == condorcet_winner:
            continue
        else:
            if candidates_copeland[i][j] > candidates_copeland[j][i]:
                out_degree[i] = out_degree[i] + 1

winner_Copeland = 0
for i in range(1, len(out_degree)):
    if out_degree[i] > out_degree[winner_Copeland]:
        winner_Copeland = i
        
#breaking ties lexicographic
for i in range(0, len(out_degree)):
    if out_degree[i] == out_degree[winner_Copeland]:
        if i > winner_Copeland:
            winner_Copeland = i
            
winner_Copeland = winner_Copeland + 1
print("Copeland winner: Course", winner_Copeland)


# In[ ]:




