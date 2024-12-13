import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def process_puzzles_solved_llm(json_path):
    df = pd.read_json(json_path)
    num_seeds = len(np.unique(df['seed']))
    # Calculate success rates
    success_yellow_count = (df['solved_yellow'] == True).sum() / 750
    success_green_count = (df['solved_green'] == True).sum() / 750
    success_blue_count = (df['solved_blue'] == True).sum() / 750
    success_purple_count = (df['solved_purple'] == True).sum() / 750
    success_overall_count = (df['solved_overall'] == True).sum() / 750

    # count_list = [success_yellow_count, success_green_count, success_blue_count, success_purple_count, success_overall_count]
    # count_list = [ct / num_seeds for ct in count_list]
    return [success_yellow_count, success_green_count, success_blue_count, success_purple_count, success_overall_count]

def process_puzzles_solved_emb(json_path):
    df = pd.read_json(json_path)
    df['yellow_solved_in_5'] = df['yellow_solved_at'] < 5
    df['green_solved_in_5'] = df['green_solved_at'] < 5

    df['blue_solved_in_5'] = df['blue_solved_at'] < 5
    df['purple_solved_in_5'] = df['purple_solved_at'] < 5
    df['puzzle_solved_in_5'] = df['yellow_solved_in_5'] & df['green_solved_in_5'] & df['blue_solved_in_5'] & df['purple_solved_in_5']

    success_yellow_count = (df['yellow_solved_in_5'] == True).sum() / 250
    success_green_count = (df['green_solved_in_5'] == True).sum() / 250
    success_blue_count = (df['blue_solved_in_5'] == True).sum() / 250
    success_purple_count = (df['purple_solved_in_5'] == True).sum() / 250
    success_overall_count = (df['puzzle_solved_in_5'] == True).sum() / 250

    
    return [success_yellow_count, success_green_count, success_blue_count, success_purple_count, success_overall_count]


def plot_puzzles_solved(exp_name_json_dict):
    fig, ax = plt.subplots(figsize=(10, 5))
    bar_width = 0.1

    # Initialize an index for the x-axis
    r = np.arange(len(exp_name_json_dict.items()))

    
    # Define the colors using hex color codes
    colors = ['#fbd400', '#69e352', '#5492ff', '#df7bea', '#A9A9A9'] # Yellow, Green, Blue, Purple, Grey
    for idx, (exp_name, path) in enumerate(exp_name_json_dict.items()):
        if 'GPT' in path:
            solved_counts = process_puzzles_solved_llm(path)
        else:
            solved_counts = process_puzzles_solved_emb(path)

        for count, color in zip(solved_counts, colors):
            if color == "#A9A9A9":
                print(f"[{exp_name}] Overall: {count}")

        # Plot each bar for the current experiment
        for i, (solved_count, color) in enumerate(zip(solved_counts, colors)):
            bars = ax.bar(r[idx] + i * bar_width, solved_count, color=color, width=bar_width, edgecolor=color)
            # Add the text label above each bar
            # for bar in bars:
            #     ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{solved_count:.2f}',
            #             ha='center', va='bottom')
    
    # Add labels, title, and legend
    ax.set_xlabel('Model', fontweight='bold')
    ax.set_xticks(r + bar_width * (len(solved_counts) - 1) / 2)
    ax.set_xticklabels(exp_name_json_dict.keys())
    ax.set_ylabel('Average Success Rate', fontweight='bold')
    ax.set_title('Average Success Rate per Category by Model')
    ax.set_ylim(0, 1)

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)
    # Create legend & Show graphic
    plt.legend(['Yellow', 'Green', 'Blue', 'Purple', 'Overall'], loc='upper left')
    plt.show()


success_barchart_dict = {
    'BERT_base': 'SentenceTransformerBaseline_model-bert-base-nli-mean-tokens_results.json',
    'BERT_repl': 'SWAPNIKA-SentenceTransformerBaseline_model-bert-base-nli-mean-tokens_results.json',
    'RoBERTa_base': 'SentenceTransformerBaseline_model-all-roberta-large-v1_results.json',
    'RoBERTa_repl': 'SWAPNIKA-SentenceTransformerBaseline_model-all-roberta-large-v1_results.json',
    'MiniLM_base': 'SentenceTransformerBaseline_model-all-MiniLM-L6-v2_results.json',
    'MiniLM_repl': 'SWAPNIKA-SentenceTransformerBaseline_model-all-MiniLM-L6-v2_results.json',
    'MPNet_base': 'SentenceTransformerBaseline_model-all-mpnet-base-v2_results.json',
    'MPNet_repl': 'SWAPNIKA-SentenceTransformerBaseline_model-all-mpnet-base-v2_results.json',
    
    
    
    
    # 'GPT 3.5': 'IterativeGPTSolver_gpt-3.5-turbo-1106_cot-False_results.json',
    # 'GPT 3.5 (CoT) ': 'IterativeGPTSolver_gpt-3.5-turbo-1106_cot-True_results.json',
    # 'GPT 4': 'IterativeGPTSolver_gpt-4-1106-preview_cot-False_results.json',
    # 'GPT 4 (CoT)': 'IterativeGPTSolver_gpt-4-1106-preview_cot-True_results.json',
    # 'GPT 4 (CoT) Challenge': 'OneShotGPTSolver_gpt-4-1106-preview_cot-True_results.json',
    # 'GPT 3 Challenge': 'OneShotGPTSolver_gpt-3.5-turbo-1106_cot-False_results.json',
}

plot_puzzles_solved(success_barchart_dict)

