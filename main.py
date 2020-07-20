from environment import Environment


env = Environment(render_game=True, human_input=True)
done = False
while not done:
    done = env.check_events()
    env.update2(1)
    env.render()
env.end()