#! /usr/bin/python3
import discord
import random
from typing import Dict
from time import sleep


class Chatter:
    def hello(self):
        self._send_message(
            "Welcome to our movie casino! Please, play your movies and place your bets")

    def movie_add_success(self, movie: str):
        variants = [f"`{movie}` in game!",
                    f"Well, if you insits...",
                    f"Oh, I've seen that. Good choice",
                    f"Attention please, we have a new film: `{movie}`",
                    f"`{movie}`. Affirmative. Something else?"
                    ]
        self._send_message(random.choice(variants))

    def vote_success(self) -> None:
        variants = [f"Here we go, thank you",
                    f"Got you. Next please",
                    f"Ok",
                    f"Accepted. Good luck!",
                    f"Feel lucky? Ok, I'll take your bet"]
        self._send_message(random.choice(variants))

    def peek_result(self, movies2id: Dict(str, int), stats: Dict(int, int), winner_id: int) -> None:
        self._send_message(
            "Attention, please. The stakes are accepted. Let's roll!")
        id2movie = dict((v, k) for k, v in movies2id.items())
        self.show_stats(id2movie, stats)
        self._send_message("And the winner is...")
        sleep(5)
        self._send_message(
            f"{movies2id[winner_id]}! Congratulations! Thanks for the game, everyone. See you later")

    def show_stats(self, id2movie: Dict(int, str), stats: Dict(int, int)):
        STAT_WORM_LEN = 20
        ordered_ids = sorted(id2movie.keys())
        total_score = sum(stats.values())
        msg = f""
        for id in ordered_ids:
            partition = (stats[id] / total_score)
            fill_worm = int(STAT_WORM_LEN * partition)
            percents = partition * 100
            msg += f"{id}. {id2movie[id]}:" + "#" * fill_worm + " " * \
                (STAT_WORM_LEN - fill_worm) + f"{percents:.2}%\n"
        self._send_message(msg)

    def movie_already_exists(self) -> None:
        self._send_message("The movie is already in game!")

    def movie_limit_reached(self) -> None:
        self._send_message(
            "You've already played all your movies. You can replace one of them though")

    def repeated_vote(self) -> None:
        self._send_message("You've already place a bet for this movie")

    def vote_limit_reached(self) -> None:
        self._send_message(
            "You are out of chips! Maybe you wish to change one of your bets?")

    def no_self_vote(self) -> None:
        self._send_message(
            "Aye-aye. Our rules say you can't vote for your own movie")

    def invalid_vote_id(self) -> None:
        self._send_message(
            "There is no movie with such id. Your bet is rejected")

    def invalid_revote_id(self) -> None:
        self._send_message(
            "I can't replace that. You haven't vote for this movie!")

    def invalid_movie_change_id(self) -> None:
        self._send_message(
            "Try to cheat? You haven't played this movie! Carefull, please")

    def _send_message(self, msg: str) -> None:
        pass
