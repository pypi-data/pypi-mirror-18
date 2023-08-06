"""
Copyright 2016 Deepgram

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from . import Loss

###############################################################################
class CategoricalCrossentropy(Loss):
	""" Categorical crossentropy loss, used for 1-of-N classification.
	"""

	###########################################################################
	@classmethod
	def get_name(cls):
		""" Returns the name of the loss function.
		"""
		return 'categorical_crossentropy'

	###########################################################################
	def get_loss(self, backend):

		if backend.get_name() == 'keras':
			return 'categorical_crossentropy'
		else:
			raise ValueError('Unsupported backend "{}" for loss function "{}"'
				.format(backend.get_name(), self.get_name()))

### EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF.EOF
