import pygetwindow as gw
import pyautogui
import sys
import cv2
import numpy as np
import neat
import pickle
import os
import time

from properties import load
from game_controls import start_combo, game_input
from game_states import update_states, check_failure_state
from fixed_queue import FixedQueue
from character import Character
from properties import *

def get_frame():
	bbox = GAME_WINDOW["x_pos"], GAME_WINDOW["y_pos"], GAME_WINDOW["width"], GAME_WINDOW["height"]
	frame = np.array(pyautogui.screenshot(region=bbox))
				  
	return frame

def init(roi_validate=True):
	global GAME_WINDOW, CHARACTER_QUEUE

	load()
	
	# Open DeSmuME
	window_title = [title for title in gw.getAllTitles() if EMULATOR in title][0]
	window = gw.getWindowsWithTitle(window_title)[0]
	window.activate()	
	pyautogui.sleep(1)
	window = gw.getActiveWindow()

	GAME_WINDOW["x_pos"] = GAME_WINDOW_OFFSET["x_offset"] + window.left
	GAME_WINDOW["y_pos"] = GAME_WINDOW_OFFSET["y_offset"] + window.top

	# Validate cv boxes if entering and leaving roi are correct
	if roi_validate:
		local_dir = os.path.dirname(__file__)

		validate1 = cv2.imread(os.path.join(local_dir, "mario.png"))
		validate2 = cv2.imread(os.path.join(local_dir, "baby_mario.png"))

		cv2.rectangle(validate1, (ENTERING_ROI["x_pos"], ENTERING_ROI["y_pos"]), (ENTERING_ROI["x_pos"]+ENTERING_ROI["width"], ENTERING_ROI["y_pos"]+ENTERING_ROI["height"]), (0, 255, 0), 2)
		cv2.rectangle(validate1, (LEAVING_ROI["x_pos"], LEAVING_ROI["y_pos"]), (LEAVING_ROI["x_pos"]+LEAVING_ROI["width"], LEAVING_ROI["y_pos"]+LEAVING_ROI["height"]), (255, 0, 0), 2)
		cv2.rectangle(validate2, (ENTERING_ROI["x_pos"], ENTERING_ROI["y_pos"]), (ENTERING_ROI["x_pos"]+ENTERING_ROI["width"], ENTERING_ROI["y_pos"]+ENTERING_ROI["height"]), (0, 255, 0), 2)
		cv2.rectangle(validate2, (LEAVING_ROI["x_pos"], LEAVING_ROI["y_pos"]), (LEAVING_ROI["x_pos"]+LEAVING_ROI["width"], LEAVING_ROI["y_pos"]+LEAVING_ROI["height"]), (255, 0, 0), 2)

		cv2.imshow("Validation 1", validate1)
		cv2.imshow("Validation 2", validate2)

		# Prompt the user for confirmation
		if pyautogui.confirm(text="Proceed?", title="Roi Validation Check", buttons=("Yes", "No")) != "Yes":
			cv2.destroyAllWindows() 
			sys.exit("Validation failed")

		cv2.destroyAllWindows() 

def predict(net, character_queue, timestamp):
	inputs = character_queue.queue
	if character_queue.max_size > len(inputs):
		inputs += (character_queue.max_size - len(inputs)) * [Character.EMPTY]

	output = net.activate(*inputs, timestamp)
	decision = output.index(max(output))

	if 1 == decision:
		game_input(A_KEY)

	elif 2 == decision:
		game_input(B_KEY)

	elif 3 == decision:
		game_input(X_KEY)

	elif 4 == decision:
		game_input(Y_KEY)

def run_copy_flower(genome, config):
	character_queue = FixedQueue(max_size=4)
	net = neat.nn.FeedForwardNetwork.create(genome, config)

	frame = get_frame()
	duration = time.time()
	while check_failure_state(frame): 
		frame = get_frame()
		character_queue = update_states(frame, character_queue)
		predict(net, character_queue, time.time())

	genome.fitness = time.time() - duration

def eval_genomes(genomes, config):
	for (genome_id, genome) in genomes:
		genome.fitness = 0
		run_copy_flower(genome, config)

def run_neat(config, generations=50, run_last_checkpoint=False):
	checkpoints_dir = "checkpoints"
	
	# Create a NEAT population
	p = neat.Population(config)
	
	# If requested, restore from the last checkpoint
	if run_last_checkpoint:
		checkpoint_files = [f for f in os.listdir(checkpoints_dir) if f.startswith("neat-checkpoint-")]
		if checkpoint_files:
			latest_checkpoint_file = max(checkpoint_files)
			p = neat.Checkpointer.restore_checkpoint(os.path.join(checkpoints_dir, latest_checkpoint_file))
		# else: start from scratch
	
	# Add reporters to the population
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	p.add_reporter(neat.StdOutReporter(True))  # Output statistics to console
	p.add_reporter(neat.Checkpointer(1, filename_prefix=os.path.join(checkpoints_dir, "neat-checkpoint-")))

	winner = p.run(eval_genomes, generations)
	with open("best_model.pickle", "wb") as f:
		pickle.dump(winner, f)

def end():
	pass

if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, "config.txt")

	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
						 neat.DefaultSpeciesSet, neat.DefaultStagnation,
						 config_path)
	
	init()
	run_neat(config)
	end()