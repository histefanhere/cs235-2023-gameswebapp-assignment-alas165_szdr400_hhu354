from pathlib import Path
from typing import List

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Publisher, Game, Genre, Review, User


# This manages the session to the database and lets us very simply interface with SQLAlchemy
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class DatabaseRepository(AbstractRepository):
    def __init__(self, session_factory):
        self.__scm = SessionContextManager(session_factory)

    def close_session(self):
        self.__scm.close_current_session()

    def reset_session(self):
        self.__scm.reset_session()

    def add_publisher(self, publisher: Publisher):
        with self.__scm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def add_game(self, game: Game):
        with self.__scm as scm:
            scm.session.merge(game)
            scm.commit()

    def get_games(self) -> List[Game]:
        """ Returns the list of games. """
        return self.__scm.session.query(Game).all()

    def get_game(self, id: int) -> Game:
        """ Returns the game with the given id from the repository. """
        game = None
        with self.__scm as scm:
            try:
                game = scm.session.query(Game).filter(Game._Game__game_id == id).first()
            except NoResultFound:
                pass
        return game

    def get_number_of_games(self):
        """ Returns the number of games that exist in the repository. """
        pass

    def get_genres(self) -> list[Genre]:
        """ Returns the list of genres. """
        pass

    def get_tags(self) -> list[str]:
        """ Returns the list of tags. """
        pass

    def search_games(self, price: float = float('inf'),
                    #  release_date: (int, str idk),
                    tags: list[str] = None,
                    recommendations: int = 0,
                    genre: Genre = None ) -> list[Game]:
        """ Returns the list of games that match the given criteria. """
        pass
    
    def get_user(self, username: str):
        """ Gets a user from the repository. """
        pass
    
    def add_user(self, user):
        """ Adds a user to the repository. """
        pass
    
    def add_review(self, review):
        """ Adds a review to the repository. """
        pass


def populate(data_path: Path, repo: AbstractRepository):
    publisher = Publisher("Activision")
    repo.add_publisher(publisher)

    game = Game(0, "Call of Duty® 4: Modern Warfare®")

    game.publisher = publisher
    game.release_date = "Nov 12, 2007"
    game.price = 9.99
    game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of the Call of Duty® series, delivers the most intense and cinematic action experience ever. Call of Duty 4: Modern Warfare arms gamers with an arsenal of advanced and powerful modern day firepower and transports them to the most treacherous hotspots around the globe to take on a rogue enemy group threatening the world. As both a U.S Marine and British S.A.S. soldier fighting through an unfolding story full of twists and turns, players use sophisticated technology, superior firepower and coordinated land and air strikes on a battlefield where speed, accuracy and communication are essential to victory. The epic title also delivers an added depth of multiplayer action providing online fans an all-new community of persistence, addictive and customizable gameplay. Authentic Advanced Weaponry - Featuring an available arsenal of more than 70 new and authentic weapons and gear from assault rifles with laser sites, claymore mines, .50 caliber sniper rifles, and M-249 SAW machine guns. With accessories like night-vision goggles and ghillie suits, for maximum concealment, Call of Duty 4: Modern Warfare has players locked and loaded to accomplish the mission. Coordinated Assault and Support - Delivering the most visceral action thriller ever, the title covers modern battle from the soldier to the satellite, where the need for air support is critical to success. The adrenaline rush deployment enlists gamers to fast-rope from tactical helicopters, ride in an armada of attack choppers, utilize jets to remove enemy strongholds and even engage hostiles from thousands of feet above the ground inside a state of the art aerial gunship. Cinematic Quality Graphics and Sound - Featuring stunning next-generation graphics, players will be drawn into the cinematic intensity of Call of Duty 4: Modern Warfare. Amazing special effects, including realistic depth of field, rim-lighting, character self-shadowing, texture streaming as well as physics-enabled effects will enlist players into the most photo-realistic gaming experience. Combine the lifelike graphics and the realistic battle chatter with the Call of Duty award-winning sound design and players will face battle as they have never before. Unparalleled Depth to Multiplayer - Multiplayer builds from the success of Call of Duty 2 delivering a persistent online experience for greater community interaction. Featuring create-a-class options allowing players to customize gear that is best suited for play, to experience points enabling unlockables and perks, all the way to matchmaking and leaderboards for the latest in tracking, Call of Duty 4: Modern Warfare's multiplayer is set to deliver easily accessible and addictive online play for all."
    game.languages = ['English', 'French', 'German', 'Italian', 'Spanish - Spain']
    game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    game.website_url = "http://www.charlieoscardelta.com/"

    game.windows = True
    game.mac = True
    game.linux = False

    game.achievements = 0
    game.developer = "Infinity Ward"
    game.categories = ['Single-player', 'Multi-player']

    # genre: Action

    # tags: "FPS,Action,Multiplayer,Shooter,Singleplayer,First-Person,Classic,Military,War,PvP,Great Soundtrack,Linear,Story Rich,Modern,Co-op,Atmospheric,Controller,Moddable,Competitive,Zombies"

    repo.add_game(game)
