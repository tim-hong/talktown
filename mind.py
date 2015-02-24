import random


class Mind(object):
    """A person's mind."""

    def __init__(self, subject):
        """Initialize a Mind object."""
        self.subject = subject
        if self.subject.mother:  # Person object
            self.memory = self._init_ex_nihilo_memory()
        else:  # PersonExNihilo object
            self.memory = self._init_memory()

    def _init_memory(self):
        """Determine a person's base memory capability, given their parents'."""
        config = self.subject.game.config
        if random.random() < config.memory_heritability:
            takes_after = random.choice([self.subject.mother, self.subject.father])
            memory = random.normalvariate(takes_after.memory, config.memory_heritability_sd)
        else:
            takes_after = None
            memory = random.normalvariate(config.memory_mean, config.memory_sd)
        if self.subject.male:  # Men have slightly worse memory (studies show)
            memory -= config.memory_sex_diff
        if memory > config.memory_cap:
            memory = config.memory_cap
        elif memory < config.memory_floor_at_birth:
            memory = config.memory_floor_at_birth
        feature_object = Feature(value=memory, inherited_from=takes_after)
        return feature_object

    def _init_ex_nihilo_memory(self):
        """Determine this person's base memory capability."""
        config = self.subject.game.config
        memory = random.normalvariate(config.memory_mean, config.memory_sd)
        if self.subject.male:  # Men have slightly worse memory (studies show)
            memory -= config.memory_sex_diff
        if memory > config.memory_cap:
            memory = config.memory_cap
        elif memory < config.memory_floor:
            memory = config.memory_floor
        feature_object = Feature(value=memory, inherited_from=None)
        return feature_object


class Feature(float):
    """A feature representing a person's memory capability and metadata about that."""

    def __init__(self, value, inherited_from):
        """Initialize a Feature object.

        @param value: A float representing the value, on a scale from -1 to 1, of a
                      person's memory capability.
        @param inherited_from: The parent from whom this memory capability was
                               inherited, if any.
        """
        super(Feature, self).__init__()
        self.inherited_from = inherited_from

    def __new__(cls, value, inherited_from):
        """Do float stuff."""
        return float.__new__(cls, value)