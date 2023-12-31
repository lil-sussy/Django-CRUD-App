import json
from django.http import JsonResponse
import traceback
import sys

import datahub.pipelines.hub as pipe
from datahub.pipelines.hub import ApiRequest
from datahub.decorators import jwt_role_required
import datahub.pipelines.hub as pipe
from datahub.pipelines.hub import ApiResponse
from datahub.pipelines.hub import check_permission_create, check_permission_update, check_permission_delete, check_permission_fetch, check_permission_fetch_all

"""_summary_
@params request: 
@description 
@returns 
"""
def view_tree(request):
  if request.method == 'GET':
    return JsonResponse(pipe.get_view_tree(), safe=False)

"""_summary_
@params request: django request object whom body follows ./restapirequest.json pattern. The request should contain a jwt token and a non-empty reference
@description API route api/execute/ that performs the requested actions on the data bases
@returns a django response following ./restapiresponse.json pattern with or without data depending on the action performed
"""
@jwt_role_required  # AMAZING PYTHON FEATURE
def execute(request):
  if request.method == 'POST':
    req: ApiRequest = ApiRequest(json.loads(request.body))
    action = req.action
    view_name = req.view_name
    row = req.row
    
    if action == 'create':
      try:
        if check_permission_create(request.user, view_name, row):
          action_performed = pipe.insert(view_name, row)
          if (action_performed):
            return ApiResponse(200, "Succesfuly created element with", None).json_response()
          else:
            return ApiResponse(400, "Unable to perform action", None).json_response()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", None).json_response()
      except:
        traceback.print_exception(*sys.exc_info())
        return ApiResponse(500, "Could not create element", None).json_response()

    elif action == 'update':
      try:
        if check_permission_update(request.user, view_name, row):
          action_performed = pipe.update(view_name, row)
          if (action_performed):
            return ApiResponse(200, "Succesfuly updated element with id ", None).json_response()
          else:
            return ApiResponse(400, "Unable to perform action", None).json_response()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", None).json_response()
      except:
        traceback.print_exception(*sys.exc_info())
        return ApiResponse(500, "Could not update element with", None).json_response()
    
    elif action == 'fetch_all':
      try:
        if check_permission_fetch_all(request.user, view_name, row):
          fetched_data = pipe.fetch_all(view_name)
          if (not fetched_data is None):
            return ApiResponse(200, "Succesfuly retrieved elements", fetched_data).json_response()
          else:
            return ApiResponse(400, "No data found with this query", None).json_response()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", fetched_data).json_response()
      except:
        traceback.print_exception(*sys.exc_info())
        return ApiResponse(400, "No data found with this query", None).json_response()
    
    elif action == 'fetch':
      try:
        if check_permission_fetch(request.user, view_name, row):
          fetched_data = pipe.fetch(view_name, row)
          if (not fetched_data is None):
            return ApiResponse(200, "Succesfuly retrieved element", fetched_data).json_response()
          else:
            return ApiResponse(400, "No data found with this query", None).json_response()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", fetched_data).json_response()
      except:
        traceback.print_exception(*sys.exc_info())
        return ApiResponse(400, "No data found with this query", None).json_response()
    
    elif action == 'remove':
      try:
        if check_permission_delete(request.user, view_name, row):
          action_performed = pipe.delete(view_name, row)
          if (action_performed):
            return ApiResponse(200, "Succesfuly retrieved element with id ", None).json_response()
          else:
            return ApiResponse(400, "Unable to perform action", None).json_response()
        else:
          return ApiResponse(403, "Error: User is not allowed to perform this action", None).json_response()
      except:
        traceback.print_exception(*sys.exc_info())
        return ApiResponse(500, "Could not delete element", None).json_response()
    else:
      return JsonResponse({"error": "Invalid method"}, status=400)