bowlabels = ['No BOW','Intersection of BOWs', 'Union of BOWs', 'Intersection + Union of BOWs']
nglabels = ['No Ngrams','Intersection of character ngrams', 'Union of character ngrams', 'Intersection + Union of character ngrams']


for i in range(0,3+1):
    for j in range(0,3+1):

        bow = bowlabels[i]
        ng = nglabels[j]


        total_num = 0
        total_found = 0
        total_rank = 0
        total_rank_found = 0
        try:
            print("Looking for " + 'out/rank.'+str(i)+'.'+str(j)+'.csv')
            with open('out/rank.'+str(i)+'.'+str(j)+'.csv','r') as f:
                for line in f:
                    id,rank,found = line.replace("\n","").split(",")
                    total_num += 1
                    total_found += int(found)
                    total_rank += int(rank)
                    total_rank_found += 0 if int(found) == 0 else int(rank)

            avg_rank = total_rank / total_num
            avg_rank_found = total_rank_found / total_found

            print(bow)
            print(ng)

            print("Number of examples: \t\t" + str(total_num))
            print("Total Found:\t\t\t\t"+str(total_found))
            print("Recall:\t\t\t\t\t\t"+ str(total_found/(total_num)))
            print("Average Rank For Correct:\t\t\t\t" + str(avg_rank_found))
            print("Average Rank:\t\t\t\t" + str(avg_rank))

            print("")
            print("")
            print("")
            print("")

        except:
            pass



