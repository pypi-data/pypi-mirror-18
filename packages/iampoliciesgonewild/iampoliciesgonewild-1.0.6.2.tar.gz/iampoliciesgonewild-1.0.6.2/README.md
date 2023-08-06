# IAMPoliciesGoneWild

This is a python implementation of the IAM Policy Expander Minimizer.

# Install:

`pip install iampoliciesgonewild`

# Usage:

```python
from iampoliciesgonewild import expand_policy
from iampoliciesgonewild import minimize_policy

policy = {
        "Statement": [{
            "Action": ["swf:res*"],
            "Resource": "*",
            "Effect": "Allow"
          }]
      }
      
expanded_policy = expand_policy(policy=policy)
>>> Start size: 131. End size: 286
print(expanded_policy == {
        "Statement": [{
            "Action": [
              "swf:respondactivitytaskcanceled",
              "swf:respondactivitytaskcompleted",
              "swf:respondactivitytaskfailed",
              "swf:responddecisiontaskcompleted"
            ],
            "Resource": "*",
            "Effect": "Allow"
          }]
      })
>>> True

minimized_policy = minimize_policy(policy=expanded_policy, minchars=3)
>>> Skipping prefix r because length of 1
>>> Skipping prefix re because length of 2
>>> Skipping prefix r because length of 1
>>> Skipping prefix re because length of 2
>>> Skipping prefix r because length of 1
>>> Skipping prefix re because length of 2
>>> Skipping prefix r because length of 1
>>> Skipping prefix re because length of 2
>>> Start size: 286. End size: 131

print(minimized_policy == policy)
>>> True
```

