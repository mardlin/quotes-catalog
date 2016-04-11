from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from pprint import pprint

engine = create_engine('sqlite:///quotes.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a dummy user
User1 = User(name="Bort", email="bort@email.com",
             picture='https://placeholder.it/100/100')
session.add(User1)
session.commit()

# Create an array with content for starting the site
categories = [
    [
        Category(name='Work'),
        [
            Item(
                author="George S. Patton",
                description="""A good plan violently executed now is better
                than a perfect plan executed next week.""",
                name="A good plan..."
                ),
            Item(
                author="",
                description="""A man with a limp can climb a mountain, as
                long as he gives himself time.""",
                name="A man with..."
                )
        ]
    ],
    [
        Category(name='Technology'),
        [
            Item(
                author="Marshall McLuhan",
                description="""Our Age of Anxiety is, in great
                part, the result of trying to do today's job with
                yesterday's tools and yesterday's concepts.""",
                name="Our Age of Anxiety..."
                ),
            Item(
                author="Kevin Kelly",
                description="""The way to build a complex system
                that works is to build it from very simple systems
                that work.""",
                name="The way to build..."
                )
        ]
    ],
    [
        Category(name='Life'),
        [
            Item(
                author="Samuel Johnson",
                description="""We cannot tell the precise moment when
                    friendship is formed. As in filling a vessel drop by
                    drop, there is at last a drop which makes it run over;
                    so in a series of kindnesses there is at last one
                    which makes the heart run over.""",
                name="We cannot tell..."
                ),
            Item(
                author="Walt Whitman",
                description="""Do I contradict myself? Very
                well then I contradict myself... I am large, I contain
                multitudes.""",
                name="Do I contradict myself..."
                ),
            Item(
                author="Marcus Aurelius",
                description="""The art of living is more
                like wrestling than dancing, in so far as it stands
                ready against the accidental and the unforeseen, and
                is not apt to fall.""",
                name="The art of living..."
            )
        ]
    ]
]

#  Assign all of the pre-populated entries to the dummy user
for category in categories:
    current_category = category[0]
    session.add(current_category)
    for item in category[1]:
        item.category = current_category
        item.user = User1
        session.add(item)
    session.commit()
