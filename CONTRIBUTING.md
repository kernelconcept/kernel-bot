# Guidelines

Contributing to the Kernel bot is easy and truly open to everyone (but of course, mainly to Kernel devs!).

Therefore, one should follow these guidelines to get along with the actual codebase:

## Asimov's rule over Kernel Bot

You might haven't known but along Asimov's three rules to apply for every alive robot, there are a few other rules written
by him for our bot ! (cool right ? :sunglasses:) Here they are:

### By the UX shall the bot swear !

The bot might not act uncool in front of other Kernel members. Acting uncool includes:

* No replies at all
* Crashing thus, not being available until the sysadmin reboots it
* Replying with grammar mistakes, or in an uncool manner.

These rules must not be broken. As the main dev of this project (@afranche), I might give you these advices to avoid that:

* *Check !* Just like the old times when we were learning C. Double check is not an option. First, you will probably avoid
grammar mistakes that made the replies ugly. Then, you will avoid some potential exceptions user will discover in your place
(And that would be such a shame ..!)

* *Test !* Nothing is better than writing tests (Or testing yourself, if it doesn't takes up that much time.). It will help you
avoid a thousand crashes by giving you a first look at potential bugs and exceptions.

* *Code safely !* Let's be honest: Nobody cares about the amount of code you're writing for one function (Except if it really becomes
unreadable, that would be an issue, for *us*.) if this function is *safe*. Safe = 100% of returning a predictable output.
People tends to provide so much strange inputs to our programs sometimes, we wouldn't want our program to have an unpredictable behaviour
if it happens. Even if your control structure resembles something like : "Accept one exact input, trash the others." It's fine, because it's
*predictable*.

* *Imagination !* Most of the time in life when we heard cool stuff, it was because we weren't expecting it. The same happens here,
surprise users !

### Don't cheat ! (Mechanical tuning > Turbocharging)

We all know tuning a car to its finest parts is way harder but better and cleaner than turbocharging. This is the same in code.

When thinking about optimizations, first think of the algorithm.

### Ordered, fast and accessible

Access to the database must be properly schemed and mustn't pose any trouble. Let's say we want to access the redis db from the website.

Given we plan to add asynchronous support, we plan at requesting change on a key at a time T (Also, think of a request as taking 3T time to give its response.).

If aside, the server is accessing the same resource to read it instead. If it is at time T+4, it won't cause any problem since the key will be freed (Remember, it only takes 3T.).

However, if it is at time T or T+[ 1 , 3 ], it will cause a data race condition.

Here's the point: Lock your keys when using them, but free them also ! We don't want the resource to be definitly locked but only for the time it's being requested.

- Master @afranche