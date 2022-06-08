import time
import retro
import argparse
import pandas as pd

from pathlib import Path
from pynput import keyboard
from gym.wrappers import Monitor

states = {
        0: 'states/1P_DK_Shroom_Solo',
        1: 'states/1P_DK_Shroom_R1.state'
    }

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rec_path", default="./gameplay_rec", type=Path)
    parser.add_argument("--state_idx", default=0, type=int)
    
    args = parser.parse_args()
    return args

class ManualController():
    def __init__(self, env, rec_path):
        self.rec_path = rec_path
        self.rec_folder = rec_path / str(int(time.time()))
        self.env = Monitor(env, self.rec_folder, force=True, 
                    video_callable=lambda episode_id: True, )
        self._delay_ms = 15 # magic number for displaying the game real-time
        self.record = True
        self.episode_summary = None
        self.action = [0] * len(env.buttons)
        self.key_mapping = self._get_key_mapping(env.buttons)

    def _get_key_mapping(self, buttons):
        key_mapping = {
            'Key.up': buttons.index('UP'),
            'Key.down': buttons.index('DOWN'),
            'Key.left': buttons.index('LEFT'),
            'Key.right': buttons.index('RIGHT'),
            'z': buttons.index('A'),
            'x': buttons.index('B'),
            'a': buttons.index('X'),
            's': buttons.index('Y')
        }
        return key_mapping

    def _set_key(self, key):
        if key in self.key_mapping.keys():
            key_index = self.key_mapping[key]
            self.action[key_index] = 1
            
    def _unset_key(self, key):
        if key in self.key_mapping.keys():
            key_index = self.key_mapping[key]
            self.action[key_index] = 0

    def _store_summary(self, info, action):
        tmp_info = info.copy()
        tmp_info['action'] = str(action)
        if self.episode_summary is None:
            self.episode_summary = pd.DataFrame(tmp_info, index=[0])
        else:
            info_df = pd.DataFrame(tmp_info, index=[len(self.episode_summary)])
            self.episode_summary = pd.concat([self.episode_summary, info_df])

    def _save_summary(self, episode_nb=0):
        csv_save_path = f'{self.rec_folder}/openaigym.episode_summary.{episode_nb}.csv'
        self.episode_summary.to_csv(csv_save_path, index=False)

    def on_press(self, key):
        if key == keyboard.Key.esc:
            # Stop listener
            self.record = False
            return False
        try:
            if isinstance(key, keyboard.Key):
                self._set_key(str(key))
            else:
                self._set_key(key.char)
        except AttributeError:
            # Special char go brrr
            pass

    def on_release(self, key):
        try:
            if isinstance(key, keyboard.Key):
                self._unset_key(str(key))
            else:
                self._unset_key(key.char)
        except AttributeError:
            # Special char go brrr
            pass

    def start_key_listener(self):
        # Collect events until released
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

    def play(self):
        print('#'*69)
        print('WARN: In order to control the game select the console window.')
        print('Steering: arrow keys   Accelerate: x key   Decelerate: z key')
        print('#'*69)
        self.start_key_listener()
        for episode_nb in range(5):
            if not self.record:
                # If the ESC button is pressed
                # before the last episode
                break
            done = False
            self.env.reset()
            # Run one episode until its done
            while self.record and not done:
                self.env.render()
                _, _, done, info = self.env.step(self.action)
                self._store_summary(info, self.action)
                time.sleep(self._delay_ms/1000)
            self._save_summary(episode_nb)
        self.env.close()

if __name__ == '__main__':
    args = parse_args()
    env = retro.make(game='SuperMarioKart-Snes', state=states[args.state_idx])

    mc_hammer = ManualController(env, args.rec_path)
    mc_hammer.play()