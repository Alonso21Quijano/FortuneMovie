#! /usr/bin/python3
import random
from pydantic import BaseModel
from typing import Union
from .chatter import Chatter


class MoviesManagerParams(BaseModel):
    init_score: int = 0
    vote_inc_score: int = 0
    vote_limit: int = 0
    suggestion_limit: int = 0
    allow_self_vote: bool = False


class MoviesManager:
    def MoviesManager(self, params: MoviesManagerParams, chatter: Chatter) -> None:
        self._params = params
        self._user_movies = {}
        self._user_votes = {}
        self._movies2id = {}
        self._chatter = chatter

    def add_movie(self, user_id: int, movie: str) -> None:
        if not self._check_valid_movie_add(user_id, movie):
            return
        if user_id not in self._user_movies:
            self._user_movies[user_id] = []
        self._movies2id[movie] = len(self._movies2id)
        self._user_movies[user_id].extend([self._movies2id[movie]])
        self._chatter.movie_add_success()

    def add_vote(self, user_id: int, movie_id: int) -> None:
        if not self._check_valid_vote_add(user_id, movie_id):
            return
        if user_id not in self._user_votes:
            self._user_votes[user_id] = []
        self._user_votes[user_id].extend([movie_id])
        self._chatter.vote_success()

    def change_movie(self, user_id: int, old_movie_id: int, new_movie: str) -> None:
        if not self._check_movie_change_possible(user_id, old_movie_id, new_movie):
            return
        for movie, id in self._movies2id.items():
            if id == old_movie_id:
                self._movies2id.pop(movie)
                self._movies2id[new_movie] = old_movie_id
        for votes in self._user_votes:
            if old_movie_id in votes:
                votes.remove(old_movie_id)
        self._chatter.movie_add_success()

    def revote(self, user_id: int, prev_vote: int, new_vote: int) -> None:
        if not self._check_revote_possible(user_id, prev_vote):
            return
        self._user_votes[user_id].remove(prev_vote)
        if not self._check_valid_vote_add(user_id, new_vote):
            self._user_votes[user_id].extend([prev_vote])
        else:
            self._user_votes[user_id].extend([new_vote])
        self._chatter.vote_success()

    def get_movie_id(self, movie: str) -> Union(int, None):
        return None if movie not in self._movies2id else self._movies2id[movie]

    def peek_movie(self) -> None:
        ids = self._movies2id.values()
        weights = {id: self._params.init_score for id in ids}
        for votes in self._user_votes:
            for vote in votes:
                weights[vote] += self._params.vote_inc_score
        winner_id = random.choices(ids, [weights[id] for id in ids])
        self._chatter.peek_result(self._movies2id, weights, winner_id)

    def _check_valid_movie_add(self, user_id: int, movie: str) -> bool:
        if movie in self._movies2id:
            self._chatter.movie_already_exists()
            return False
        if (user_id in self._user_movies and
                len(self._user_movies[user_id]) >= self._params.suggestion_limit):
            self._chatter.movie_limit_reached()
            return False
        return True

    def _check_valid_vote_add(self, user_id: int, movie_id: int) -> bool:
        if user_id in self._user_votes and movie_id in self._user_votes[movie_id]:
            self._chatter.repeated_vote()
            return False
        if user_id in self._user_votes and self._user_votes[user_id] >= self._params.vote_limit:
            self._chatter.vote_limit_reached()
            return False
        if (not self._params.allow_self_votes and user_id in self._user_movies and
                movie_id in self._user_movies[user_id]):
            self._chatter.no_self_vote()
            return False
        if movie_id >= self._movies2id.size():
            self._chatter.invalid_vote_id()
            return False
        return True

    def _check_movie_change_possible(self, user_id: int, prev_id: int, new_movie: str) -> bool:
        if user_id not in self._user_movies or prev_id not in self._user_movies[user_id]:
            self._chatter.invalid_movie_change_id()
            return False
        if new_movie in self._movies2id:
            self._chatter.movie_already_exists()
            return False
        return True

    def _check_revote_possible(self, user_id: int, prev_vote: int) -> bool:
        if user_id not in self._user_votes or prev_vote not in self._user_votes[user_id]:
            self._chatter.invalid_revote_id()
            return False
        return True
