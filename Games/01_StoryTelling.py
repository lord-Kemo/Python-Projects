def get_input(wordtype: str) -> str:
    '''Get the user's input and return it.'''
    user_input: str = input(f"Enter a {wordtype}: ")
    return user_input


noun1 = get_input("noun (imaginary charachter like wizard, witch, etc.)")
noun2 = get_input("noun (imaginary place like forest, castle, etc.)")
verb = get_input("verb (action word like create, make, etc.)")
verb2 = get_input("verb (action word like explore, travel, etc.)")


story = f"""

Once upon a time, there was a wise old {noun1} who lived deep in the heart of an {noun2}.
The {noun1} had spent centuries learning the secrets of magic, and its greatest joy was to {verb} potions that could heal, transform, or even grant wishes.

Every morning, the {noun1} would wake up with the first rays of sunlight streaming through the trees of the {noun2}.
Birds would sing cheerful songs, and magical creatures would gather around to watch the {noun1} {verb}.
But the {noun1} wasn't content to stay in one place; it also loved to {verb2} the vast, mysterious lands surrounding the {noun2}.

One day, while on a journey to collect rare herbs, the {noun1} stumbled upon a hidden glade where the air shimmered with golden light.
In the center of the glade stood a fountain bubbling with liquid that sparkled like stardust.
Curious, the {noun1} carefully filled a vial with the liquid and decided to study its properties.

Back at the {noun2}, the {noun1} began experimenting with the stardust-like liquid.
To its astonishment, the potion it brewed glowed with a brilliance never seen before.
When the {noun1} tested the potion, a tree in its yard grew golden leaves that hummed with magic.
News of the {noun1}'s discovery spread far and wide.

Soon, adventurers, royalty, and even other {noun1}s traveled to the {noun2} to see the wonder for themselves.
The {noun1} shared its knowledge with anyone who came in peace, asking only for one thing in return: a story from their land.

Over time, the {noun1}'s home became a gathering place for the most remarkable tales in the world.
The {noun1}, surrounded by stories and magic, lived happily, creating potions and exploring new mysteries.

And so, the {noun1}'s legend grew, whispered across kingdoms as the one who {verb} potions and {verb2} new horizons, forever curious and kind.

"""


print(story)