import pickle
from model.game_manager import GameManager
from ex.critic_explainer import ExplainByCriticTree

def read_and_print_pickle():  
    try:
        with open('game_state_data.pkl', 'rb') as f:
            datas = pickle.load(f)
            count = 0
            for data  in datas:
                action = data["action"]
                game_state = data["game_state"]
                if action >= 15 and action <= 29: # 15-29 are the actions to buy cards
                    count += 1
                    print(action)
                else:
                    print("---")
                    
            print(f"Number of buy actions: {count}")
            print(f"Total number of actions: {len(datas)}")
            print(f"Percentage of buy actions: {count/len(datas)}")         
            
            
            
            
            
            
    except Exception as e:
        print(f"Error loading pickle file: {e}")

if __name__ == "__main__":
    read_and_print_pickle()     
      