# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  StateProcessor.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: gtourdia <gtourdia@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/19 13:41:54 by gtourdia        #+#    #+#               #
#  Updated: 2026/03/19 13:42:39 by gtourdia        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from src import State


class AbstractStateProcessor(ABC):
    """ Process a zone to its next step """
    @abstractmethod
    def process(state: State) -> State:
        pass


class StateProcessor(AbstractStateProcessor):
    def process(state: State) -> State:
        pass