INTRO = """
This program will generate multiple paragraphs for a fairy tale given the title, characters and key points.

<end>

Title: Little Red Cap
Audience: children
Characters: Little Red Cap, The wolf, Mother, Grandma, Lumberjacks
Characters descriptions:
Red Riding Hood is a little girl who got her nickname because of her beanie. A good, little girl lives with her mother. She didn’t listen to mother’s advice and went to my grandmother through the forest.
Wolf is the negative hero, dangerous predator. An evil and bloodthirsty beast, a cunning and clever deceiver. A greedy and insatiable predator, through cunning and deceit, found out my grandmother's address.
Mother is the working middle-aged woman. A caring woman, worried about her mother's health, sends gifts to her.
Grandma is the  old sick woman. A helpless old woman who loves her granddaughter very much. She does not hear and see well, so she falls for the deception of the wolf.
Lumberjacks are workers who are engaged in logging. Courageous and strong lumberjacks who were passing by heard a noise, jumped into the hut and killed the wolf, freed the grandmother and granddaughter from his belly.

Plots:
ABSENTATION: Little Red Cap leaves her house for her Grandma.
INTERDICTION: Mother punishes Little Red Cap so that she, going to her Grandma, does not leave the path.
VIOLATION: Little Red Cap leaves the path to collect flowers.
RECONNAISSANCE: The wolf asks Little Red Cap where she is going and where her Grandma lives.

<First Paragraph>: Once upon a time there was a sweet little girl.
Everyone who saw her liked her, but most of all her grandmother, who did not know what to give the child next.
Once she gave her a little cap made of red velvet. Because it suited her so well,
and she wanted to wear it all the time, she came to be known as Little Red Cap.
One day her mother said to her, "Come Little Red Cap. Here is a piece of cake and
a bottle of wine. Take them to your grandmother. She is sick and weak, and they will do her well.
Mind your manners and give her my greetings.

<Second Paragraph>: Behave yourself on the way, and do not leave the path,
or you might fall down and break the glass, and then there will be nothing for your sick grandmother."
Little Red Cap promised to obey her mother. The grandmother lived out in the woods, a half hour from the village.

<Third Paragraph>: When Little Red Cap entered the woods a wolf came up to her. She did not know what a wicked animal he was, and was not afraid of him.

<Fourth Paragraph>: She did not know what a wicked animal he was, and was not afraid of him.
"Good day to you, Little Red Cap."
"Thank you, wolf."
"Where are you going so early, Little Red Cap?"
"To grandmother's."
"And what are you carrying under your apron?"
"Grandmother is sick and weak, and I am taking her some cake and wine. We baked yesterday, and they should give her strength."
"Little Red Cap, just where does your grandmother live?"

<end>

Title: {name}
Audience: {audience}
Characters: {heroes}
Characters descriptions:
{heroes_desc}
Plots:
{}
<First Paragraph>:"""
