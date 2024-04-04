from fsm import FSM

def main():
    fsm = FSM.from_json("json/fsm.json")
    fsm.visualize("output/fsm")
    fsm.to_json("json/out.json")

if __name__ == "__main__":
    main()