"""
Main API for Vega-lite spec generation.

DSL mapping Vega types to IPython traitlets.
"""
import os
import functools
import operator

import traitlets as T
import pandas as pd

from .utils import visitors
from .utils._py3k_compat import string_types
from .utils import node

from . import expr
from . import schema

from .schema import AggregateOp
from .schema import AxisConfig
from .schema import AxisOrient
from .schema import Axis
from .schema import Bin
from .schema import CellConfig
from .schema import Config
from .schema import Data
from .schema import DataFormat
from .schema import DateTime
from .schema import EqualFilter
from .schema import FacetConfig
from .schema import FacetGridConfig
from .schema import FacetScaleConfig
from .schema import FontStyle
from .schema import FontWeight
from .schema import HorizontalAlign
from .schema import LegendConfig
from .schema import Legend
from .schema import MarkConfig
from .schema import NiceTime
from .schema import OneOfFilter
from .schema import OverlayConfig
from .schema import RangeFilter
from .schema import Scale
from .schema import ScaleConfig
from .schema import SortField
from .schema import SortOrder
from .schema import StackOffset
from .schema import TimeUnit
from .schema import UnitSpec
from .schema import UnitEncoding
from .schema import VerticalAlign

#*************************************************************************
# Channel Aliases
#*************************************************************************
from .schema import X, Y, Row, Column, Color, Size, Shape, Text, Label, Detail, Opacity, Order, Path
from .schema import Encoding, Facet


def use_signature(Obj):
    """Apply call signature and documentation of Obj to the decorated method"""
    def decorate(f):
        # call-signature of f is exposed via __wrapped__.
        # we want it to mimic Obj.__init__
        f.__wrapped__ = Obj.__init__
        f._uses_signature = Obj

        # Supplement the docstring of f with information from Obj
        f.__doc__ += Obj.__doc__[Obj.__doc__.index('\n'):]
        return f
    return decorate


#*************************************************************************
# Formula wrapper
# - makes field a required first argument of initialization
# - allows expr trait to be an Expression and processes it properly
#*************************************************************************
class Formula(schema.Formula):
    expr = T.Union([T.Unicode(), T.Instance(expr.Expression)],
                    allow_none=True, default_value=None,
                    help=schema.Formula.expr.help)

    def __init__(self, field, expr=None, **kwargs):
        super(Formula, self).__init__(field=field, expr=expr, **kwargs)

    def _finalize(self, **kwargs):
        """Finalize object: convert expr expression to string if necessary"""
        if isinstance(self.expr, expr.Expression):
            self.expr = repr(self.expr)
        super(Formula, self)._finalize(**kwargs)


#*************************************************************************
# Transform wrapper
# - allows filter trait to be an Expression and processes it properly
#*************************************************************************
class Transform(schema.Transform):
    filter = T.Union([T.Unicode(),
                      T.Instance(expr.Expression),
                      T.Instance(schema.EqualFilter),
                      T.Instance(schema.RangeFilter),
                      T.Instance(schema.OneOfFilter),
                      T.List(T.Union([T.Unicode(),
                                      T.Instance(expr.Expression),
                                      T.Instance(schema.EqualFilter),
                                      T.Instance(schema.RangeFilter),
                                      T.Instance(schema.OneOfFilter)]))],
                     allow_none=True, default_value=None,
                     help=schema.Transform.filter.help)

    def _finalize(self, **kwargs):
        """Finalize object: convert filter expressions to string"""
        convert = lambda f: repr(f) if isinstance(f, expr.Expression) else f
        self.filter = convert(self.filter)
        if isinstance(self.filter, list):
            self.filter = [convert(f) for f in self.filter]
        super(Transform, self)._finalize(**kwargs)


#*************************************************************************
# Top-level Objects
#*************************************************************************
class TopLevelMixin(object):
    @staticmethod
    def _png_output_available():
        return node.vl_cmd_available('vl2png')

    @staticmethod
    def _svg_output_available():
        return node.vl_cmd_available('vl2svg')

    def savechart(self, outfile, filetype=None):
        """Save a chart to file, in either png, svg, json, or html format.

        Note that png/svg output requires several nodejs packages to be
        installed and correctly configured. Before running this, you must
        have nodejs and cairo on your system and use the node package manager
        to install the ``canvas`` and ``vega-lite`` packages.

        If you are using anaconda, you can set it up this way:

            $ conda create -n node-env -c conda-forge python=2.7 cairo nodejs altair
            $ source activate node-env
            $ npm install canvas vega-lite

        The node binaries used here (``vl2vg``, ``vl2png``, ``vl2svg``) will be
        installed in the node root directory, which should be automatically
        detected by this function.

        Parameters
        ----------
        outfile : str
            The output filename
        filetype : str (optional)
            The filetype to use. One of ('svg', 'png', 'json', 'html').
            If not specified, it will be inferred from outfile.
        """
        if filetype is None:
            try:
                base, ext = os.path.splitext(outfile)
                filetype = ext[1:]
            except AttributeError:
                raise ValueError('filetype could not be inferred')

        if filetype in node.SUPPORTED_FILETYPES:
            node.savechart(self, outfile, filetype)
        elif filetype == 'json':
            if hasattr(outfile, 'write'):
                outfile.write(self.to_json())
            else:
                with open(outfile, 'w') as f:
                    f.write(self.to_json())
        elif filetype == 'html':
            if hasattr(outfile, 'write'):
                outfile.write(self.to_html())
            else:
                with open(outfile, 'w') as f:
                    f.write(self.to_html())
        else:
            supported = _node.SUPPORTED_FILETYPES + ['json', 'html']
            raise ValueError('Cannot save chart of type {0}; supported'
                             'extensions are {1}'.format(filetype, supported))

    def to_html(self, template=None, title=None, **kwargs):
        """Emit a stand-alone HTML document containing this chart.

        Parameters
        ----------
        template : string
            The HTML template to use. This should have a format method, which
            accepts a "spec" and "title" argument. Note that a standard Python
            format string meets these requirements.
            By default, uses altair.utils.html.DEFAULT_TEMPLATE.
        title : string
            The title to use in the document. Default is "Vega-Lite Chart"
        kwargs :
            additional keywords to be passed to the template

        Returns
        -------
        html : string
            A string of HTML representing the chart
        """
        from .utils.html import to_html
        return to_html(self.to_dict(), template=template, title=title, **kwargs)

    def _to_code(self, data=None):
        """Emit the CodeGen object used to export this chart to Python code."""
        # do not call _finalize(), as we want the output code
        # to reflect the exact input
        return visitors.ToCode().visit(self, data=data)

    def to_altair(self, data=None):
        """Emit the Python code as a string required to created this Chart."""
        return str(self._to_code(data=data))

    # transform method
    @use_signature(schema.Transform)
    def transform_data(self, *args, **kwargs):
        """Set the data transform by keyword args."""
        return self._update_subtraits('transform', *args, **kwargs)

    # Configuration methods
    @use_signature(schema.Config)
    def configure(self, *args, **kwargs):
        """Set chart configuration"""
        return self._update_subtraits('config', *args, **kwargs)

    @use_signature(AxisConfig)
    def configure_axis(self, *args, **kwargs):
        """Configure the chart's axes by keyword args."""
        return self._update_subtraits(('config', 'axis'), *args, **kwargs)

    @use_signature(CellConfig)
    def configure_cell(self, *args, **kwargs):
        """Configure the chart's cell's by keyword args."""
        return self._update_subtraits(('config', 'cell'), *args, **kwargs)

    @use_signature(LegendConfig)
    def configure_legend(self, *args, **kwargs):
        """Configure the chart's legend by keyword args."""
        return self._update_subtraits(('config', 'legend'), *args, **kwargs)

    @use_signature(OverlayConfig)
    def configure_overlay(self, *args, **kwargs):
        """Configure the chart's overlay by keyword args."""
        return self._update_subtraits(('config', 'overlay'), *args, **kwargs)

    @use_signature(MarkConfig)
    def configure_mark(self, *args, **kwargs):
        """Configure the chart's marks by keyword args."""
        return self._update_subtraits(('config', 'mark'), *args, **kwargs)

    @use_signature(ScaleConfig)
    def configure_scale(self, *args, **kwargs):
        """Configure the chart's scales by keyword args."""
        return self._update_subtraits(('config', 'scale'), *args, **kwargs)

    @use_signature(FacetConfig)
    def configure_facet(self, *args, **kwargs):
        """Configure the chart's scales by keyword args."""
        return self._update_subtraits(('config', 'facet'), *args, **kwargs)

    @use_signature(AxisConfig)
    def configure_facet_axis(self, *args, **kwargs):
        """Configure the facet's axes by keyword args."""
        return self._update_subtraits(('config', 'facet', 'axis'),
                                     *args, **kwargs)

    @use_signature(CellConfig)
    def configure_facet_cell(self, *args, **kwargs):
        """Configure the facet's cells by keyword args."""
        return self._update_subtraits(('config', 'facet', 'cell'),
                                     *args, **kwargs)

    @use_signature(FacetGridConfig)
    def configure_facet_grid(self, *args, **kwargs):
        """Configure the facet's grid by keyword args."""
        return self._update_subtraits(('config', 'facet', 'grid'),
                                     *args, **kwargs)

    @use_signature(FacetScaleConfig)
    def configure_facet_scale(self, *args, **kwargs):
        """Configure the facet's scales by keyword args."""
        return self._update_subtraits(('config', 'facet', 'scale'),
                                     *args, **kwargs)

    # Display related methods
    def _ipython_display_(self):
        from IPython.display import display
        from vega import VegaLite
        display(VegaLite(self.to_dict()))

    def display(self):
        from IPython.display import display
        display(self)

    def serve(self, ip='127.0.0.1', port=8888, n_retries=50, files=None,
              jupyter_warning=True, open_browser=True, http_server=None,
              **html_kwargs):
        """Open a web browser and visualize the chart

        Parameters
        ----------
        html : string
            HTML to serve
        ip : string (default = '127.0.0.1')
            ip address at which the HTML will be served.
        port : int (default = 8888)
            the port at which to serve the HTML
        n_retries : int (default = 50)
            the number of nearby ports to search if the specified port
            is already in use.
        files : dictionary (optional)
            dictionary of extra content to serve
        jupyter_warning : bool (optional)
            if True (default), then print a warning if this is used
            within the Jupyter notebook
        open_browser : bool (optional)
            if True (default), then open a web browser to the given HTML
        http_server : class (optional)
            optionally specify an HTTPServer class to use for showing the
            figure. The default is Python's basic HTTPServer.
        """
        from .utils.server import serve
        html = self.to_html(**html_kwargs)
        serve(html, ip=ip, port=port, n_retries=n_retries,
              files=files, jupyter_warning=jupyter_warning,
              open_browser=open_browser, http_server=http_server)

    def _finalize_data(self):
        """
        This function is called by _finalize() below. It checks whether the
        data attribute contains expressions, and if so it extracts the
        appropriate data object and generates the appropriate transforms.
        """
        if isinstance(self.data, expr.DataFrame):
            columns = self.data._cols
            calculated_cols = self.data._calculated_cols
            filters = self.data._filters
            self.data = self.data._data
            if columns is not None and isinstance(self.data, pd.DataFrame):
                self.data = self.data[columns]
            if calculated_cols:
                self.transform_data(calculate=[Formula(field, expr=exp)
                                               for field, exp
                                               in calculated_cols.items()])
            if filters:
                filters = [repr(f) for f in filters]
                if len(filters) == 1:
                    self.transform_data(filter=filters[0])
                else:
                    self.transform_data(filter=filters)


class Chart(schema.ExtendedUnitSpec, TopLevelMixin):
    _data = None

    # use specialized version of Encoding and Transform
    encoding = T.Instance(Encoding, allow_none=True, default_value=None,
                          help=schema.ExtendedUnitSpec.encoding.help)
    transform = T.Instance(Transform, allow_none=True, default_value=None,
                           help=schema.ExtendedUnitSpec.transform.help)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new):
        if isinstance(new, string_types):
            self._data = Data(url=new)
        elif (new is None or isinstance(new, pd.DataFrame)
              or isinstance(new, expr.DataFrame) or isinstance(new, Data)):
            self._data = new
        else:
            raise TypeError('Expected DataFrame or altair.Data, got: {0}'.format(new))

    skip = ['data', '_data']

    def __init__(self, data=None, **kwargs):
        super(Chart, self).__init__(**kwargs)
        self.data = data

    def __dir__(self):
        return [m for m in dir(self.__class__) if m not in dir(T.HasTraits)]

    @use_signature(MarkConfig)
    def mark_area(self, *args, **kwargs):
        """Set the mark to 'area' and optionally specify mark properties"""
        self.mark = 'area'
        return self.configure_mark(*args, **kwargs)

    @use_signature(MarkConfig)
    def mark_bar(self, *args, **kwargs):
        """Set the mark to 'bar' and optionally specify mark properties"""
        self.mark = 'bar'
        return self.configure_mark(*args, **kwargs)

    @use_signature(MarkConfig)
    def mark_errorBar(self, *args, **kwargs):
        """Set the mark to 'errorBar' and optionally specify mark properties"""
        self.mark = 'errorBar'
        return self.configure_mark(*args, **kwargs)

    @use_signature(MarkConfig)
    def mark_line(self, *args, **kwargs):
        """Set the mark to 'line' and optionally specify mark properties"""
        self.mark = 'line'
        return self.configure_mark(*args, **kwargs)

    @use_signature(MarkConfig)
    def mark_point(self, *args, **kwargs):
        """Set the mark to 'point' and optionally specify mark properties"""
        self.mark = 'point'
        return self.configure_mark(*args, **kwargs)

    @use_signature(MarkConfig)
    def mark_rule(self, *args, **kwargs):
        """Set the mark to 'rule' and optionally specify mark properties"""
        self.mark = 'rule'
        return self.configure_mark(*args, **kwargs)

    @use_signature(MarkConfig)
    def mark_text(self, *args, **kwargs):
        """Set the mark to 'text' and optionally specify mark properties"""
        self.mark = 'text'
        return self.configure_mark(*args, **kwargs)

    @use_signature(MarkConfig)
    def mark_tick(self, *args, **kwargs):
        """Set the mark to 'tick' and optionally specify mark properties"""
        self.mark = 'tick'
        return self.configure_mark(*args, **kwargs)

    @use_signature(MarkConfig)
    def mark_circle(self, *args, **kwargs):
        """Set the mark to 'circle' and optionally specify mark properties"""
        self.mark = 'circle'
        return self.configure_mark(*args, **kwargs)

    @use_signature(MarkConfig)
    def mark_square(self, *args, **kwargs):
        """Set the mark to 'square' and optionally specify mark properties"""
        self.mark = 'square'
        return self.configure_mark(*args, **kwargs)

    @use_signature(Encoding)
    def encode(self, *args, **kwargs):
        """Define the encoding for the Chart."""
        return self._update_subtraits('encoding', *args, **kwargs)

    def _finalize(self, **kwargs):
        self._finalize_data()
        # data comes from wrappers, but self.data overrides this if defined
        if self.data is not None:
            kwargs['data'] = self.data
        super(Chart, self)._finalize(**kwargs)

    def __add__(self, other):
        if isinstance(other, Chart):
            lc = LayeredChart()
            lc += self
            lc += other
            return lc
        else:
            raise TypeError('Can only add Charts/LayeredChart to Chart')

    @classmethod
    def from_dict(cls, spec):
        if 'layers' in spec:
            return LayeredChart.from_dict(spec)
        elif 'facet' in spec:
            return FacetedChart.from_dict(spec)
        else:
            return super(Chart, cls).from_dict(spec)

    @classmethod
    def load_example(cls, name):
        """Load an example chart

        Initialize a chart object from one of the built-in examples

        Parameters
        ----------
        example : string
            The example ID or filename, e.g. ``"line"`` or ``"line.json"``

        Returns
        -------
        chart : Chart, LayeredChart, or FacetedChart
            The Chart object containing the example
        """
        from .examples import load_example
        spec = load_example(name)
        return cls.from_dict(spec)


class LayeredChart(schema.LayerSpec, TopLevelMixin):
    _data = None

    # Use specialized version of Chart and Transform
    layers = T.List(T.Instance(Chart), allow_none=True, default_value=None,
                    help=schema.LayerSpec.layers.help)
    transform = T.Instance(Transform, allow_none=True, default_value=None,
                           help=schema.LayerSpec.transform.help)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new):
        if isinstance(new, string_types):
            self._data = Data(url=new)
        elif (new is None or isinstance(new, pd.DataFrame)
              or isinstance(new, expr.DataFrame) or isinstance(new, Data)):
            self._data = new
        else:
            raise TypeError('Expected DataFrame or altair.Data, got: {0}'.format(new))

    skip = ['data', '_data']

    def __init__(self, data=None, **kwargs):
        super(LayeredChart, self).__init__(**kwargs)
        self.data = data

    def __dir__(self):
        return [m for m in dir(self.__class__) if m not in dir(T.HasTraits)]

    def set_layers(self, *layers):
        self.layers = list(layers)
        return self

    def _finalize(self, **kwargs):
        self._finalize_data()
        # data comes from wrappers, but self.data overrides this if defined
        if self.data is not None:
            kwargs['data'] = self.data
        super(LayeredChart, self)._finalize(**kwargs)

    def __iadd__(self, layer):
        if self.layers is None:
            self.layers = [layer]
        else:
            self.layers = self.layers + [layer]
        return self


class FacetedChart(schema.FacetSpec, TopLevelMixin):
    _data = None

    # Use specialized version of Facet, spec, and Transform
    facet = T.Instance(Facet, allow_none=True, default_value=None,
                       help=schema.FacetSpec.facet.help)
    spec = T.Union([T.Instance(LayeredChart), T.Instance(Chart)],
                   allow_none=True, default_value=None,
                   help=schema.FacetSpec.spec.help)
    transform = T.Instance(Transform, allow_none=True, default_value=None,
                           help=schema.FacetSpec.transform.help)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new):
        if isinstance(new, string_types):
            self._data = Data(url=new)
        elif (new is None or isinstance(new, pd.DataFrame)
              or isinstance(new, expr.DataFrame) or isinstance(new, Data)):
            self._data = new
        else:
            raise TypeError('Expected DataFrame or altair.Data, got: {0}'.format(new))

    skip = ['data', '_data']

    def __init__(self, data=None, **kwargs):
        super(FacetedChart, self).__init__(**kwargs)
        self.data = data

    def __dir__(self):
        return [m for m in dir(self.__class__) if m not in dir(T.HasTraits)]

    @use_signature(Facet)
    def set_facet(self, *args, **kwargs):
        """Define the facet encoding for the Chart."""
        return self._update_subtraits('facet', *args, **kwargs)

    def _finalize(self, **kwargs):
        self._finalize_data()
        # data comes from wrappers, but self.data overrides this if defined
        if self.data is not None:
            kwargs['data'] = self.data
        super(FacetedChart, self)._finalize(**kwargs)
