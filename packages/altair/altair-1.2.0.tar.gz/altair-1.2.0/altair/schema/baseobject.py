import json

import pandas as pd
import traitlets as T

from ..utils._py3k_compat import string_types

_attr_template = "Attribute not found: {0}. Valid keyword arguments for this class: {1}"


class BaseObject(T.HasTraits):

    skip = []

    def __init__(self, **kwargs):
        all_traits = list(self.traits())
        for k in kwargs:
            if k not in all_traits:
                raise KeyError(_attr_template.format(k, all_traits))
        super(BaseObject, self).__init__(**kwargs)

    @classmethod
    def _infer_keywords(cls, *args, **kwargs):
        """Utility to initialize object from args and kwargs

        Arguments are converted to keyword arguments by inferring the keyword
        from their type.
        Keyword arguments are converted to the correct Instance class
        if required.
        """
        # TODO: can we make this more efficient & less fragile?
        def is_simple_union(trait):
            """Return True if trait is, e.g. Union(Class, List(Class))"""
            return (isinstance(trait, T.Union) and
                    len(trait.trait_types) == 2 and
                    isinstance(trait.trait_types[0], T.Instance) and
                    isinstance(trait.trait_types[1], T.List) and
                    trait.trait_types[0].klass == trait.trait_types[1]._trait.klass)

        def get_class(trait):
            if isinstance(trait, T.Instance):
                return trait.klass
            elif is_simple_union(trait):
                return trait.trait_types[0].klass
            else:
                return None

        traits = cls.class_traits()
        classes = {n: get_class(t) for n, t in traits.items()}

        # Turn all keyword arguments to the appropriate class
        for name, arg in kwargs.items():
            Trait = classes.get(name, None)
            if Trait is not None and not isinstance(arg, Trait):
                try:
                    kwargs[name] = Trait(arg)
                except (TypeError, T.TraitError):
                    pass  # errors will handled by traitlets below

        # find forward/backward mapping among unique classes
        name_to_trait = {}
        while classes:
            name, trait = classes.popitem()
            if trait is None:
                continue
            if trait not in set.union(set(classes.values()),
                                      set(name_to_trait.values())):
                name_to_trait[name] = trait
        trait_to_name = {t: n for n, t in name_to_trait.items()}

        # Update all arguments
        for arg in args:
            name = trait_to_name.get(type(arg), None)
            if name is None:
                raise ValueError("{0}: Unable to infer argument name for {1}".format(cls, arg))
            elif name in kwargs:
                raise ValueError("{0}: {1} specified both by arg and kwarg".format(cls, name))
            else:
                kwargs[name] = arg
        return kwargs

    def _update_traits(self, **kwargs):
        for key, val in kwargs.items():
            self.set_trait(key, val)
        return self

    def _update_inferred_traits(self, *args, **kwargs):
        kwargs = self._infer_keywords(*args, **kwargs)
        return self._update_traits(**kwargs)

    def _update_subtraits(self, attrs, *args, **kwargs):
        """Update sub-traits without overwriting other traits"""
        if not (args or kwargs):
            return self
        if isinstance(attrs, string_types):
            attrs = (attrs,)
        if len(attrs) == 0:
            self._update_inferred_traits(*args, **kwargs)
        else:
            attr = attrs[0]
            if attr not in self.traits():
                raise ValueError('{0} has no trait {1}'.format(self, attr))
            trait = getattr(self, attr)
            if trait is None:
                trait = self.traits()[attr].klass()
            setattr(self, attr, trait._update_subtraits(attrs[1:], *args, **kwargs))
        return self

    def __contains__(self, key):
        try:
            value = getattr(self, key)
        except AttributeError:
            return False

        # comparison to None will break, so check DataFrame specifically
        if isinstance(value, pd.DataFrame):
            return True
        elif value is not None:
            if isinstance(value, (int, float, bool)):
                return True
            else:
                return bool(value)
        else:
            return False

    def __dir__(self):
        """Customize tab completed attributes."""
        return list(self.traits())+['to_dict', 'from_dict']

    @classmethod
    def from_dict(cls, dct):
        """Instantiate the object from a valid JSON dictionary

        Parameters
        ----------
        dct : dict
            The dictionary containing a valid JSON chart specification.

        Returns
        -------
        chart : Chart object
            The altair Chart object built from the specification.
        """
        # Import here to prevent circular imports
        from ..utils.visitors import FromDict
        return FromDict().clsvisit(cls, dct)

    @classmethod
    def from_json(cls, spec):
        """Instantiate the object from a valid JSON string

        Parameters
        ----------
        spec : string
            The string containing a valid JSON chart specification.

        Returns
        -------
        chart : Chart object
            The altair Chart object built from the specification.
        """
        return cls.from_dict(json.loads(spec))

    def to_dict(self, data=True):
        """Emit the JSON representation for this object as as dict.

        Parameters
        ----------
        data : bool
            If True (default) then include data in the representation.

        Returns
        -------
        spec : dict
            The JSON specification of the chart object.
        """
        from ..utils.visitors import ToDict
        self._finalize()
        return ToDict().visit(self, data)

    def to_json(self, data=True, sort_keys=True, **kwargs):
        """Emit the JSON representation for this object as a string.

        Parameters
        ----------
        data : bool
            If True (default) then include data in the representation.
        sort_keys : bool
            If True (default) then sort the keys in the output
        **kwargs
            Additional keyword arguments are passed to ``json.dumps()``

        Returns
        -------
        spec : string
            The JSON specification of the chart object.
        """
        return json.dumps(self.to_dict(data=data), sort_keys=True, **kwargs)

    def _finalize(self, **kwargs):
        """Finalize the object, and all contained objects, for export."""
        def finalize_obj(obj):
            if isinstance(obj, BaseObject):
                obj._finalize(**kwargs)
            elif isinstance(obj, list):
                for item in obj:
                    finalize_obj(item)

        for name in self.traits():
            value = getattr(self, name)
            finalize_obj(value)
