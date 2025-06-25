import json

def format_json_string(json_string):
    try:
        parsed = json.loads(json_string)
        return json.dumps(parsed, indent=4, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"

def format_json_file(input_path, output_path=None):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        formatted_json = json.dumps(data, indent=4, ensure_ascii=False)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_json)
            print(f"Formatted JSON written to {output_path}")
        else:
            print(formatted_json)

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
# Format a JSON string
raw_json = '{"accounting":{"accumulated_wins":{"progressive":0,"regular":0,"special_prize_freespin":0},"final_balances":{"cashable":99999999,"promotional_non_restricted":99999999,"promotional_restricted":99999999},"payments":{"progressive":0,"regular":0,"special_prize_freespin":0},"play_bet":{"bet_level_index":0,"denomination_index":0,"in_credits":100,"in_currency":100,"lines_index":0},"start_balances":{"cashable":99999999,"promotional_non_restricted":99999999,"promotional_restricted":99999999},"wagers":{"cashable":100000,"promotional_non_restricted":0,"promotional_restricted":0},"wins":{"progressive":0,"regular":0,"special_prize_freespin":0}},"active_type":"default","currency":"US DOLLAR","currency_symbol":"$","emulation":false,"free_spin":{"active":false,"additional_spins_stacked":[],"base_previous_play":null,"element_count":3,"end":false,"index":0,"retrigger":false,"stacked":[],"total":5,"total_stacked":0,"win":true,"win_spins":5},"g150":{"index_reel_wild_bar_transform":[],"wild_transformed":[]},"game_name":"NewGame_CollapseLink","generic_slot":{"current_play_reel_type":1,"next_play_reel_type":0,"play_result_index":[57,119,29,32,58],"prizes":[],"reels":[[6,3,11],[2,10,6],[1,5,12],[6,3,12],[11,12,7]],"reels_name":[{"label":"Base Reels","names":[["ACE","CC","NINE"],["BB","TEN","ACE"],["AA","EE","FREE_SPIN"],["ACE","CC","FREE_SPIN"],["NINE","FREE_SPIN","KING"]]},{"label":"Wild Positions","names":[["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"],["-","-","-"]]}],"updated_bet_coins":[[{"offset":19,"type":0,"value":100},{"offset":20,"type":0,"value":250},{"offset":43,"type":0,"value":250},{"offset":45,"type":0,"value":150},{"offset":47,"type":0,"value":250},{"offset":97,"type":0,"value":100},{"offset":98,"type":0,"value":200},{"offset":101,"type":0,"value":200}],[{"offset":19,"type":0,"value":250},{"offset":20,"type":0,"value":150},{"offset":43,"type":0,"value":100},{"offset":45,"type":0,"value":200},{"offset":47,"type":0,"value":200},{"offset":97,"type":0,"value":250},{"offset":98,"type":0,"value":250},{"offset":101,"type":0,"value":200}],[{"offset":19,"type":0,"value":100},{"offset":20,"type":0,"value":100},{"offset":43,"type":0,"value":100},{"offset":45,"type":0,"value":150},{"offset":47,"type":0,"value":200},{"offset":96,"type":0,"value":150},{"offset":98,"type":0,"value":100},{"offset":101,"type":0,"value":150}],[{"offset":19,"type":0,"value":250},{"offset":20,"type":0,"value":100},{"offset":43,"type":0,"value":100},{"offset":45,"type":0,"value":250},{"offset":47,"type":0,"value":250},{"offset":97,"type":0,"value":200},{"offset":98,"type":0,"value":150},{"offset":101,"type":0,"value":250}],[{"offset":19,"type":0,"value":250},{"offset":20,"type":0,"value":200},{"offset":43,"type":0,"value":250},{"offset":45,"type":0,"value":200},{"offset":47,"type":0,"value":200},{"offset":97,"type":0,"value":100},{"offset":98,"type":2,"value":5000},{"offset":101,"type":0,"value":150}]]},"mini_game_params":null,"play_seq":41,"power_cycle":false,"progressive":[{"name":"Jackpot Link","prize":{"tier":-1,"value":0},"progressive_id":1,"tier":[2000,5000,100000,1500000]}],"replay":false,"status":"-3"}'
print(format_json_string(raw_json))

# Format a JSON file (optional output to another file)
# format_json_file("input.json", "output.json")
