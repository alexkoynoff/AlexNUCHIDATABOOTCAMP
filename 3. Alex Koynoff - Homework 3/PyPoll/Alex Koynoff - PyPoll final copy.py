import os
import csv

#path to file
pypollfile = os.path.join('..','PyPoll','election_data.csv')

#set the votes counter to zero
total_votes = 0


#make lists
candidates_list = []
num_votes = []
percentage_of_votes = []


#open as csv file
with open(pypollfile, newline="") as csvfile:
    #store file information in variable csvreader
    csvreader = csv.reader(csvfile,delimiter=',')
    #print(csvreader)
    
    #skips the header of the file
    csv_header = next(csvreader)

    for row in csvreader:
        #adds up the total votes
        total_votes +=1
        #candidate receiving the votes
        candidate_name = row[2]


        #adds votes to candidate's vote count
        if candidate_name in candidates_list:
            candidate_index = candidates_list.index(candidate_name)
            num_votes[candidate_index] = num_votes[candidate_index] + 1
        else:
            candidates_list.append(candidate_name)
            num_votes.append(1)



max_votes = num_votes[0]
max_index = 0

#calculate the percentage of votes for each of the candidates
for votes in range(len(candidates_list)):
    vote_percentage = round((num_votes[votes]/total_votes*100),2)
    percentage_of_votes.append(vote_percentage)
    if num_votes[votes] > max_votes:
        max_votes = num_votes[votes]
        max_index = votes
winner = candidates_list[max_index] #winner pick



#printing of results

print("Election Results")
print("--------------------------------------")
print(f"Total Votes: {total_votes}")
print("--------------------------------------")
for votes in range(len(candidates_list)):
    print(f"{candidates_list[votes]}: {percentage_of_votes[votes]}% ({num_votes[votes]})")
print("---------------------------")
print(f"Winner: {winner}")
print("---------------------------")



#export results to text file
export_file = os.path.join('..','PyPoll','Election_Results_Alex_Koynoff.txt')
with open(export_file,'w',newline='') as text_file:
    writer = csv.writer(text_file)

    writer.writerow(['Election Results for PyPoll by Alex Koynoff']),
    writer.writerow(["-" * 40])
    writer.writerow([f"Total Votes: {total_votes}"])
    writer.writerow(["-" * 40])
    for votes in range(len(candidates_list)):
        writer.writerow([f"{candidates_list[votes]}: {percentage_of_votes[votes]}% ({num_votes[votes]})"])
    writer.writerow(["-" * 40])
    writer.writerow([f"Winner: {winner}"])
    writer.writerow(["-" * 40])