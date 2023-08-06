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
class CertPreflightRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Push', '2016-08-01', 'CertPreflight')

	def get_AppKey(self):
		return self.get_query_params().get('AppKey')

	def set_AppKey(self,AppKey):
		self.add_query_param('AppKey',AppKey)

	def get_DeviceToken(self):
		return self.get_query_params().get('DeviceToken')

	def set_DeviceToken(self,DeviceToken):
		self.add_query_param('DeviceToken',DeviceToken)

	def get_Pass(self):
		return self.get_query_params().get('Pass')

	def set_Pass(self,Pass):
		self.add_query_param('Pass',Pass)

	def get_Body(self):
		return self.get_query_params().get('Body')

	def set_Body(self,Body):
		self.add_query_param('Body',Body)

	def get_IsDevCert(self):
		return self.get_query_params().get('IsDevCert')

	def set_IsDevCert(self,IsDevCert):
		self.add_query_param('IsDevCert',IsDevCert)