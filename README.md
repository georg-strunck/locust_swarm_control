# locust_swarm_control
Migratory locusts detect incoming objects more urgently than parallel flying or outbound objects. This feature has been analyzed and implemented in Python code to demonstrate the swarm behaviour based on these vision properties.

## Running the code
The v3 version is the cleanest version allowing swarm-only, swarm-only-extended (options A+B) and allowing to run the swarm behaviour with predators chasing.

The v2 version still includes the more elaborate swarming based on specific avoidance, centering, alignment and flocking rules. Yet this does not work as nice as the newer version.

The Swarm_Execute and Swarm_Control scripts are the beginning of making the code easier to use, defining functions and classes instead of doing all in on big while loop.

The 2D version is a non functioning test setup for checking the behaviour.
