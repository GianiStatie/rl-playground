import retro
import cv2

from src.processing.preprocessing import fetch_pipeline

if __name__ == '__main__':
    env = retro.make(game='SuperMarioKart-Snes')
    env.reset()

    pre_pipeline = fetch_pipeline([0, 112, 0, 256])

    for _ in range(1000):
        state, reward, done, info = env.step(env.action_space.sample()) # take a random action
        state = pre_pipeline.transform(state)
        cv2.imshow('frame', state)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    env.close()
    print(state.shape, info)
    print(type(state))