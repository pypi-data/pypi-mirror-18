from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from estimators.database import Base, DataBase, PrimaryMixin
from estimators.datasets import DataSet
from estimators.estimators import Estimator


class EvaluationMixin:

    """A list of common methods and attributes for evaluations"""

    def _get_proxy_object(self, obj, ProxyKlass, proxy_klass_attribute):
        """ Returns the proxy object for an input object

        If the object is already the proxy object, return it.
        Otherwise set the appropriate proxy object to the proxy object's attribute
        """
        proxy_object = obj
        if not isinstance(obj, ProxyKlass):
            proxy_object = ProxyKlass(**{proxy_klass_attribute: obj})
        return proxy_object

    @property
    def estimator(self):
        return self._estimator_proxy.estimator

    @estimator.setter
    def estimator(self, obj):
        self._estimator_proxy = self._get_proxy_object(obj, Estimator, 'estimator')

    @property
    def X_test(self):
        return self._X_test_proxy.data

    @X_test.setter
    def X_test(self, obj):
        self._X_test_proxy = self._get_proxy_object(obj, DataSet, 'data')

    @property
    def y_test(self):
        return self._y_test_proxy.data

    @y_test.setter
    def y_test(self, obj):
        self._y_test_proxy = self._get_proxy_object(obj, DataSet, 'data')

    @property
    def y_predicted(self):
        return self._y_predicted_proxy.data

    @y_predicted.setter
    def y_predicted(self, obj):
        self._y_predicted_proxy = self._get_proxy_object(obj, DataSet, 'data')


class Evaluator(EvaluationMixin):

    """Instantiates an evaluation plan.

    An evaluator object takes an estimator, X_test and y_test as params.
    Those can be DataSet objects or data in themselves.

    Once set, the evaluator aka evaluation plan runs .evaluate()
    """

    def __init__(self, **options):
        self.estimator = options.pop('estimator', None)
        self.X_test = options.pop('X_test', None)
        self.y_test = options.pop('y_test', None)
        self.y_predicted = options.pop('y_predicted', None)

        self.session = options.pop('session', None)
        if not self.session:
            db = DataBase()
            self.session = db.Session()

    def evaluate(self, persist=True):
        result = self.estimator.predict(self.X_test)

        options = {
            'y_predicted': result,
            'estimator': self.estimator,
            'X_test': self.X_test,
            'y_test': self.y_test,
        }
        er = EvaluationResult(**options)
        self.persist_results(er)
        return er

    def persist_results(self, er):

        try:
            self.session.add(er._estimator_proxy)
            self._estimator_proxy.persist()

            self.session.add(er._X_test_proxy)
            self._X_test_proxy.persist()

            self.session.add(er._y_test_proxy)
            self._y_test_proxy.persist()

            self.session.add(er._y_predicted_proxy)
            self._y_predicted_proxy.persist()
            self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()

    def __repr__(self):
        return '<Evaluator(X_test=%s estimator=%s)>' % (
            self.X_test, self.estimator)


class EvaluationResult(EvaluationMixin, PrimaryMixin, Base):

    """A database model for evaluation results.

    The EvaluationResult class is the data model for the table `result`.

    The EvaluationResult has relationships to an Estimator
    object and to 3 DataSet objects: X_test, y_test, y_predicted

    """

    __tablename__ = 'result'

    estimator_id = Column(Integer, ForeignKey('estimator.id'))
    X_test_id = Column(Integer, ForeignKey('dataset.id'), nullable=False)
    y_test_id = Column(Integer, ForeignKey('dataset.id'))
    y_predicted_id = Column(Integer, ForeignKey('dataset.id'))
    _estimator_proxy = relationship("Estimator", backref="EvaluationResult")
    _X_test_proxy = relationship("DataSet", foreign_keys=X_test_id)
    _y_test_proxy = relationship("DataSet", foreign_keys=y_test_id)
    _y_predicted_proxy = relationship("DataSet", foreign_keys=y_predicted_id)

    def __repr__(self):
        return '<EvaluationResult(id=%s X_test=%s estimator=%s)>' % (
            self.id, self.X_test, self.estimator)
