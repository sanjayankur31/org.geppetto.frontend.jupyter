from collections import defaultdict
import ipywidgets as widgets
from traitlets import (Unicode, Instance, List, Float, Dict)

from IPython.core.debugger import Tracer

# Current variables
record_variables = defaultdict(list)
current_project = None
current_experiment = None
current_model = None
current_python_model = None
events_controller = None


class EventsSync(widgets.Widget):
    _model_name = Unicode('EventsSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)
    _events = {
        'Select': 'experiment:selection_changed'
    }
    _eventsCallbacks = {}

    def __init__(self, **kwargs):
        super(EventsSync, self).__init__(**kwargs)

        self.on_msg(self._handle_event)

    def _handle_event(self, _, content, buffers):
        if content.get('event', '') == self._events['Select']:
            self.log.debug("Event triggered")
            for callback in self._eventsCallbacks[self._events['Select']]:
                try:
                    callback(content.get('data', ''),
                             content.get('groupNameIdentifier', ''))
                except Exception as e:
                    self.log.exception( "Unexpected error executing callback on event triggered:")
                    raise

    def registerToEvent(self, events, callback):
        # FIXME we should allow to add callback not only init
        for event in events:
            if event not in self._eventsCallbacks:
                self._eventsCallbacks[event] = []
            self._eventsCallbacks[event].append(callback)
            self.log.debug("Registring event " + str(event) +
                          " with callback " + str(callback))


class ExperimentSync(widgets.Widget):
    _model_name = Unicode('ExperimentSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    name = Unicode('').tag(sync=True)
    id = Unicode('').tag(sync=True)
    lastModified = Unicode('').tag(sync=True)
    state = Unicode('').tag(sync=True)

    def __init__(self, **kwargs):
        super(ExperimentSync, self).__init__(**kwargs)


class ProjectSync(widgets.Widget):
    _model_name = Unicode('ProjectSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    experiments = List(Instance(ExperimentSync)).tag(
        sync=True, **widgets.widget_serialization)

    def __init__(self, **kwargs):
        super(ProjectSync, self).__init__(**kwargs)

    def addExperiment(self, experiment):
        self.experiments = [i for i in self.experiments] + [experiment]


class StateVariableSync(widgets.Widget):
    _model_name = Unicode('StateVariableSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    units = Unicode('').tag(sync=True)
    timeSeries = List(Float).tag(sync=True)

    python_variable = None

    def __init__(self, **kwargs):
        super(StateVariableSync, self).__init__(**kwargs)

        # Add it to the syncvalues
        if 'python_variable' in kwargs and kwargs["python_variable"] is not None:
            record_variables[kwargs["python_variable"]] = self


class GeometrySync():
    # _model_name = Unicode('GeometrySync').tag(sync=True)
    # _model_module = Unicode('geppettoJupyter').tag(sync=True)

    # id = Unicode('').tag(sync=True)
    # name = Unicode('').tag(sync=True)

    # bottomRadius = Float(-1).tag(sync=True)
    # topRadius = Float(-1).tag(sync=True)
    # positionX = Float(-1).tag(sync=True)
    # positionY = Float(-1).tag(sync=True)
    # positionZ = Float(-1).tag(sync=True)
    # distalX = Float(-1).tag(sync=True)
    # distalY = Float(-1).tag(sync=True)
    # distalZ = Float(-1).tag(sync=True)
    id = ''
    name = ''

    bottomRadius = -1
    topRadius = -1
    positionX = -1
    positionY = -1
    positionZ = -1
    distalX = -1
    distalY = -1
    distalZ = -1

    python_variable = None

    def __init__(self, **kwargs):
        # super(GeometrySync, self).__init__(**kwargs)
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')

        self.bottomRadius = kwargs.get('bottomRadius')
        self.topRadius = kwargs.get('topRadius')
        self.positionX = kwargs.get('positionX')
        self.positionY = kwargs.get('positionY')
        self.positionZ = kwargs.get('positionZ')
        self.distalX = kwargs.get('distalX')
        self.distalY = kwargs.get('distalY')
        self.distalZ = kwargs.get('distalZ')

        self.python_variable = kwargs.get('python_variable')

    def get_geometry_dict(self):
        return {'id': self.id,
                'name': self.name,
                'bottomRadius': self.bottomRadius,
                'positionX': self.positionX,
                'positionY': self.positionY,
                'positionZ': self.positionZ,
                'topRadius': self.topRadius,
                'distalX': self.distalX,
                'distalY': self.distalY,
                'distalZ': self.distalZ
               }


class ModelSync(widgets.Widget):
    _model_name = Unicode('ModelSync').tag(sync=True)
    _model_module = Unicode('geppettoJupyter').tag(sync=True)

    id = Unicode('').tag(sync=True)
    name = Unicode('').tag(sync=True)
    stateVariables = List(Instance(StateVariableSync)).tag(
        sync=True, **widgets.widget_serialization)
    geometries = List(Dict).tag(
        sync=True)
    geometries_raw = []

    def __init__(self, **kwargs):
        super(ModelSync, self).__init__(**kwargs)

    def addStateVariable(self, stateVariable):
        self.stateVariables = [
            i for i in self.stateVariables] + [stateVariable]

    def addGeometries(self, geometries):
        self.geometries_raw = [i for i in self.geometries_raw] + geometries
        self.geometries = [i for i in self.geometries] + [i.get_geometry_dict() for i in geometries]

    def sync(self):
        self.send({"type": "load"})
