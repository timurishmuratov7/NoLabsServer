import {
  BiobuddyService,
  CancelablePromise,
  CheckBioBuddyEnabledResponse,
  CreateMessageResponse,
  EditMessageResponse,
  FunctionCall_Input,
  GetAvailableFunctionCallsResponse,
  LoadConversationResponse,
  SendQueryResponse,
  WorkflowSchemaModel_Output,
} from 'src/refinedApi/client';

import {getWorkflow} from 'src/features/workflow/refinedApi';

export async function getWorkflowSchema(experimentId: string): Promise<WorkflowSchemaModel_Output | null> {
  return await getWorkflow(experimentId);
}

export function checkBioBuddyEnabled(): CancelablePromise<CheckBioBuddyEnabledResponse> {
  return BiobuddyService.checkBiobuddyEnabledApiV1BiobuddyCheckBiobuddyEnabledGet();
}

export function loadConversationApi(experimentId: string): CancelablePromise<LoadConversationResponse> {
  return BiobuddyService.loadConversationApiV1BiobuddyLoadConversationGet(experimentId);
}

export function saveMessageApi(experimentId: string, messageId: string, message: string, role: string): CancelablePromise<CreateMessageResponse> {
  return BiobuddyService.createMessageApiV1BiobuddyMessageCreatePost(experimentId, messageId, message, role);
}

export function saveFunctionCallApi(experimentId: string, messageId: string, message: FunctionCall_Input, role: string): CancelablePromise<any> {
  return BiobuddyService.createFunctionCallMessageApiV1BiobuddyFunctionCreatePost(experimentId, messageId, role, message)
}

export function editMessageApi(experimentId: string, messageId: string, message: string): CancelablePromise<EditMessageResponse> {
  return BiobuddyService.editMessageApiV1BiobuddyMessageEditPost(experimentId, messageId, message);
}

export function sendQueryApi(experiment_id: string, query: string): CancelablePromise<SendQueryResponse> {
  return BiobuddyService.sendQueryApiV1BiobuddyQueryPost(experiment_id, query);
}

export function getToolsApi(): CancelablePromise<GetAvailableFunctionCallsResponse> {
  return BiobuddyService.getToolsApiV1BiobuddyToolsGet();
}
