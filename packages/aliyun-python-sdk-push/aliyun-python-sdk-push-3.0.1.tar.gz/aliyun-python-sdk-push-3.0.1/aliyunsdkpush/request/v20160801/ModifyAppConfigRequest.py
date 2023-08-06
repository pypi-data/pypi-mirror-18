# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
class ModifyAppConfigRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Push', '2016-08-01', 'ModifyAppConfig')

	def get_AppKey(self):
		return self.get_query_params().get('AppKey')

	def set_AppKey(self,AppKey):
		self.add_query_param('AppKey',AppKey)

	def get_PackageName(self):
		return self.get_query_params().get('PackageName')

	def set_PackageName(self,PackageName):
		self.add_query_param('PackageName',PackageName)

	def get_DevCertKey(self):
		return self.get_query_params().get('DevCertKey')

	def set_DevCertKey(self,DevCertKey):
		self.add_query_param('DevCertKey',DevCertKey)

	def get_DevCertPass(self):
		return self.get_query_params().get('DevCertPass')

	def set_DevCertPass(self,DevCertPass):
		self.add_query_param('DevCertPass',DevCertPass)

	def get_ProductCertKey(self):
		return self.get_query_params().get('ProductCertKey')

	def set_ProductCertKey(self,ProductCertKey):
		self.add_query_param('ProductCertKey',ProductCertKey)

	def get_ProductCertPass(self):
		return self.get_query_params().get('ProductCertPass')

	def set_ProductCertPass(self,ProductCertPass):
		self.add_query_param('ProductCertPass',ProductCertPass)

	def get_BundleId(self):
		return self.get_query_params().get('BundleId')

	def set_BundleId(self,BundleId):
		self.add_query_param('BundleId',BundleId)

	def get_BoxFlag(self):
		return self.get_query_params().get('BoxFlag')

	def set_BoxFlag(self,BoxFlag):
		self.add_query_param('BoxFlag',BoxFlag)