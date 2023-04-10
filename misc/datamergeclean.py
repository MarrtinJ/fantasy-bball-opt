import pandas as pd
from tqdm import tqdm


def main():
	df = pd.read_csv('data/dataset2.csv')
	print(df.shape)
	# iterate through all dates, call pdbruteforce on each date
	pdbruteforce(df, None)


"""
pdbruteforce
	attempts to brute force using cross products between pandas dataframes
	(very memory intensive)
"""

def pdbruteforce(df, date=None):
	date = 20191022
	df = df[df['Date']==20191022]

	# filter df to necessary rows
	df = df[['Name', 'Team', 'Position', 'Salary', 'FPTS']]
	
	df = addPosCol(df)
	print(df)

	PGs = []
	SGs = []
	Gs = []
	SFs = []
	PFs = []
	Cs = []
	Fs = []
	Utils = []

	# create dataframes for each position
	for index, player in df.iterrows():
		Utils.append(player)
		if player['PosArray'][0] == 1:
			PGs.append(player)
			Gs.append(player)
		if player['PosArray'][1] == 1:
			SGs.append(player)
			Gs.append(player)
		if player['PosArray'][2] == 1:
			SFs.append(player)
			Fs.append(player)
		if player['PosArray'][3] == 1:
			PFs.append(player)
			Fs.append(player)
		if player['PosArray'][4] == 1:
			Cs.append(player)    

	Utils = pd.DataFrame(Utils)
	Utils = Utils[['Name', 'Team', 'PosArray', 'Salary', 'FPTS']]

	PGs = pd.DataFrame(PGs)
	PGs = PGs[['Name', 'Team', 'PosArray', 'Salary', 'FPTS']]
	SGs = pd.DataFrame(SGs)
	SGs = SGs[['Name', 'Team', 'PosArray', 'Salary', 'FPTS']]
	Gs = pd.DataFrame(Gs)
	Gs.drop_duplicates(subset='Name', inplace=True)
	Gs = Gs[['Name', 'Team', 'PosArray', 'Salary', 'FPTS']]

	SFs = pd.DataFrame(SFs)
	SFs = SFs[['Name', 'Team', 'PosArray', 'Salary', 'FPTS']]
	PFs = pd.DataFrame(PFs)
	PFs = PFs[['Name', 'Team', 'PosArray', 'Salary', 'FPTS']]
	Fs = pd.DataFrame(Fs)
	Fs.drop_duplicates(subset='Name', inplace=True)
	Fs = Fs[['Name', 'Team', 'PosArray', 'Salary', 'FPTS']]

	Cs = pd.DataFrame(Cs)
	Cs = Cs[['Name', 'Team', 'PosArray', 'Salary', 'FPTS']]

	print(PGs.shape)
	print(SGs.shape)
	print(SFs.shape)
	print(PFs.shape)
	print(Cs.shape)
	print(Gs.shape)
	print(Fs.shape)
	print(Utils.shape)

	# PgSg = PGs.merge(SGs, how='cross', suffixes=('_PG', '_SG'))
	# SfPf = SFs.merge(PFs, how='cross', suffixes=('_SF', '_PF'))
	# CsGs = Cs.merge(Gs, how='cross', suffixes=('_C', '_G'))
	# FsUtils = Fs.merge(Utils, how='cross', suffixes=('_F', '_Util'))

	# print(PgSg.shape)
	# print(SfPf.shape)
	# print(CsGs.shape)
	# print(FsUtils.shape)

	# lineups1 = PgSg.merge(SfPf, how='cross')
	# print(lineups1.shape)
	# lineups2 = CsGs.merge(FsUtils, how='cross')
	# print(lineups2.shape)
	# print(lineups1)

	# lineups = lineups1.merge(lineups2, how='cross')
	# print(lineups.shape)



def addPosCol(df):
	pos_index = {'PG': 0, 'SG': 1, 'SF':2, 'PF': 3, 'C': 4}
	pos_arr = []
	for index, row in df.iterrows():
		position = [0, 0, 0, 0, 0]
		# check if Position contains '/'
		# if doesn't contain, player only has 1 position
		# if does contain player has 2 positions, split at '/'
		if row['Position'].find('/') == -1:
			playerPos = row['Position']
			idx = pos_index[playerPos]
			position[idx] = 1
			# print(row['Name'], playerPos, position)
			pos_arr.append(position)
		else:
			playerPos1, playerPos2 = row['Position'].split('/')
			# print(row['Name'], playerPos1, playerPos2)
			idx1, idx2 = pos_index[playerPos1], pos_index[playerPos2]
			position[idx1] = 1
			position[idx2] = 1
			# print(row['Name'], playerPos1, playerPos2, position)
			pos_arr.append(position)
	df.insert(3, 'PosArray', pos_arr)
	return df

if __name__ == "__main__":
	main()