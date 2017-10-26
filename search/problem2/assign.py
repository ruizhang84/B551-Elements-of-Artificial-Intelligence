#!/usr/bin/env python
import sys
import random
import copy
import math

TEAM_MAX = 3
ITER_MAX = 1000
TEMPT_MAX = 2


class Team:
    """
       A class for team operation
       including joining or removing a person
       from the team
    """

    def __init__(self):
        self.member = []
        self.name_list = set()
        self.size = 0

    def is_full(self):
        return self.size >= TEAM_MAX

    def is_empty(self):
        return self.size == 0

    def membership(self, person_name):
        return person_name in self.name_list

    def add_person(self, person):
        if self.is_full() or self.membership(person.name):
            return False

        self.member.append(person)
        self.name_list.add(person.name)
        self.size = len(self.name_list)

        return True

    def kick_out(self, person):
        if self.is_empty() or not self.membership(person.name):
            return "FAILURE"

        self.member.remove(person)
        self.name_list.remove(person.name)
        self.size = len(self.name_list)

        if self.is_empty():
            return "EMPTY"
        return "SUCCESS"

    def self_copy(self):
        team = Team()
        team.member = self.member[:]
        team.name_list = self.name_list.copy()
        team.size = self.size
        return team


class Person:
    """
       A class for peron
       including person's name and its perference
       group size, prefer to work, not to work
    """

    def __init__(self, person_name, group_size, prefer_mates, avoid_mates):
        self.name = person_name
        self.size = group_size
        self.prefer = set()
        self.avoid = set()

        for s in prefer_mates:
            self.prefer.add(s)
        for t in avoid_mates:
            self.avoid.add(t)

    def love_person(self, person_name):
        return person_name in self.prefer

    def hate_person(self, person_name):
        return person_name in self.avoid

    def love_not_exist(self, team):
        nums = 0
        for love in self.prefer:
            if not team.membership(love):
                nums += 1
        return nums

    def hate_exist(self, team):
        nums = 0
        for member in team.member:
            if self.hate_person(member):
                nums += 1
        return nums

    def love_size(self, team):
        return self.size == 0 or self.size == team.size


def read_team(input_file):
    def process_line(line):
        line = line.strip()
        return line.split(" ")

    def process_list(name_list):
        "no preference as '_' "
        if name_list == '_':
            return []
        name_list = name_list.split(',')
        return name_list

    # init
    person_list = []

    # process line by line
    with open(input_file, 'rU') as f:
        for line in f:
            temp = process_line(line)
            name, size, love, hate = temp
            size = int(size)
            love = process_list(love)
            hate = process_list(hate)
            person = Person(name, size, love, hate)
            person_list.append(person)
    return person_list


def cost_function(team):
    cost = 0
    # 1) They need k minutes to grade each assignment,
    #  so total grading time is k times number of teams.
    cost += k

    # 2) Each student who requested a specific group size
    # and was assigned to a different group size will complain to
    # the instructor after class, taking 1 minute of the instructor's time.
    for a_person in team.member:
        if not a_person.love_size(team):
            cost += 1
    # 3) Each student who is not assigned to someone they requested
    # will send a complaint email, which will take n minutes for the
    # instructor to read and respond.
    for a_person in team.member:
        cost += n * a_person.love_not_exist(team)

    # 4) Each student who is assigned to someone they requested not to work
    # with (in question 4 above) will request a meeting with the instructor to complain,
    # and each meeting will last m minutes.
    for a_person in team.member:
        cost += m * a_person.hate_exist(team)
    return cost


def total_cost(team_list):
    # total time cost of the assignmetn of teams
    total = 0
    for team in team_list:
        total += cost_function(team)
    return int(total)


def process_assignment(k, m, n, persons):
    """
       A local search to assign team
    """

    def random_assign(person_list):
        """
           randomly assign person into team
        """
        if len(person_list) == 0:
            return []
        # random pick persons
        number_to_pick = random.randint(1, TEAM_MAX)
        a_group = random.sample(
            person_list,
            min(
                number_to_pick,
                len(person_list)
            )
        )
        # assign team
        team = Team()
        for person in a_group:
            team.add_person(person)

        # make up the rest team
        new_list = [p for p in person_list if p not in a_group]
        return [team] + random_assign(new_list)

    def perturbation(team_list):
        """
           randmly perturb the current teams
           given a team, this team can split up,
           merge with another team (if possible), or
           exchange its team members with another team.
        """

        def rest_teams(choose):
            if type(choose) is list:
                return [t for t in team_list if t not in choose]
            return [t for t in team_list if t != choose]

        def team_split(a_team):
            def a_team_split(team, split_num):
                def recur_split(ans, temp, rest):
                    if len(temp) == split_num:
                        team1 = Team()
                        team2 = Team()
                        for p in team.member:
                            if p in temp:
                                team1.add_person(p)
                            else:
                                team2.add_person(p)
                        ans.extend([[team1]
                                    + [team2]
                                    + rest_teams(a_team)
                                    ])

                    for i in range(len(rest)):
                        recur_split(ans, temp[:] + [rest[i]], rest[i + 1:])
                    return

                ans = []
                temp = []
                person_in_team = [p for p in a_team.member]
                recur_split(ans, temp, person_in_team)
                return ans

            if a_team.size < 2:
                return []
            number_to_split = 1
            outcomes = []
            while number_to_split <= a_team.size / 2:
                outcomes.extend(a_team_split(
                    a_team.self_copy(),
                    number_to_split
                )
                )
                number_to_split += 1
            return outcomes

        def team_exchange(pair):
            def a_exchange(person, team_from, team_to):
                if team_to.is_full():
                    return []
                team_to.add_person(person)
                team_from.kick_out(person)

                if team_from.is_empty():
                    return [[team_to] + rest_teams(pair)]
                return [[team_from, team_to] + rest_teams(pair)]

            outcomes = []
            team_from, team_to = pair
            for person in team_from.member:
                outcomes.extend(
                    a_exchange(
                        person,
                        team_from.self_copy(),
                        team_to.self_copy()
                    )
                )
            return outcomes

        def team_merge(pair):
            team1, team2 = pair
            if team1.size + team2.size > TEAM_MAX:
                return []
            team = Team()
            for person in team1.member:
                team.add_person(person)
            for person in team2.member:
                team.add_person(person)

            return [[team] + rest_teams(pair)]

        def extend(possibility, result):
            if len(result) > 0:
                possibility.extend(result)
            return

        # random choice a team
        teams_choice = random.choice(team_list)
        teams_pair = None
        if len(team_list) > 1:
            teams_pair = random.sample(team_list, 2)

        # all the pertubation options
        possible_outcomes = [team_list]
        # extend(possible_outcomes, team_split(teams_choice))
        if teams_pair is not None:
            extend(possible_outcomes, team_exchange(teams_pair))
            extend(possible_outcomes, team_merge(teams_pair))
        return random.choice(possible_outcomes)

    def monte_carlo(team_list, tempT):
        """
           Monte Carlo Decent (general algo)
           1. S <- inital state
           2. Repeat k times
              - if Goal(s) return S
              - s' <-successor of s picked at random
              - if h(s') <= h(s) then s <- s'
                eles with prob exp(-h(s')-h(s))/T), s<-s'
           3. Return failure
        """

        def get_prob(new_list, team_list):
            return math.exp(
                -(
                    total_cost(new_list)
                    -
                    total_cost(team_list)
                )
                * 1.0
                /
                tempT
            )

        def bool_prob(prob):
            generator = random.random()
            # print generator, prob
            return generator < prob

        new_list = perturbation(team_list)
        if total_cost(new_list) <= total_cost(team_list):
            return new_list
        elif bool_prob(get_prob(new_list, team_list)):
            return new_list
        return team_list

    def decr_tempt(counter):
        return TEMPT_MAX * (1.0 - counter * 1.0 / ITER_MAX)

    # init assignment
    test_list = random_assign(persons)
    # display(test_list)
    # simulated annealing
    for i in range(ITER_MAX):
        test_list = monte_carlo(test_list, decr_tempt(i + 1))
    return test_list


def display(team_list):
    for team in team_list:
        for person in team.member:
            print person.name,
        print
    print total_cost(team_list)
    return


# ###########################
# read in data
# assert(len(sys.argv)) == 5
# input_file = "example.txt"
assert (len(sys.argv)) == 5
program, input_file, k, m, n = sys.argv
k, m, n = float(k), float(m), float(n)
person_list = read_team(input_file)

# process data
results = process_assignment(k, m, n, person_list)

# display movement
display(results)
