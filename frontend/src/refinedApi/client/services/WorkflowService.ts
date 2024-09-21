/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AllWorkflowSchemasResponse } from '../models/AllWorkflowSchemasResponse';
import type { GetComponentResponse } from '../models/GetComponentResponse';
import type { GetJobState } from '../models/GetJobState';
import type { ResetWorkflowRequest } from '../models/ResetWorkflowRequest';
import type { WorkflowSchema_Input } from '../models/WorkflowSchema_Input';
import type { WorkflowSchema_Output } from '../models/WorkflowSchema_Output';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class WorkflowService {
    /**
     * Create workflow schema
     * @param experimentId
     * @returns WorkflowSchema_Output Successful Response
     * @throws ApiError
     */
    public static createWorkflowSchemaApiV1WorkflowExperimentIdPost(
        experimentId: string,
    ): CancelablePromise<WorkflowSchema_Output> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/workflow/{experiment_id}',
            path: {
                'experiment_id': experimentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete workflow schema
     * @param workflowId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createSchemaApiV1WorkflowWorkflowIdDelete(
        workflowId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/workflow/{workflow_id}',
            path: {
                'workflow_id': workflowId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get workflow schema
     * @param workflowId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getSchemaApiV1WorkflowWorkflowIdGet(
        workflowId: string,
    ): CancelablePromise<(WorkflowSchema_Output | null)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/workflow/{workflow_id}',
            path: {
                'workflow_id': workflowId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * All workflow schemas
     * @param experimentId
     * @returns AllWorkflowSchemasResponse Successful Response
     * @throws ApiError
     */
    public static getSchemaApiV1WorkflowAllExperimentIdGet(
        experimentId: string,
    ): CancelablePromise<AllWorkflowSchemasResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/workflow/all/{experiment_id}',
            path: {
                'experiment_id': experimentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update workflow schema
     * @param requestBody
     * @returns WorkflowSchema_Output Successful Response
     * @throws ApiError
     */
    public static updateWorkflowSchemaApiV1WorkflowPut(
        requestBody: WorkflowSchema_Input,
    ): CancelablePromise<WorkflowSchema_Output> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/workflow/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Start workflow
     * @param workflowId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static startWorkflowApiV1WorkflowWorkflowIdStartPost(
        workflowId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/workflow/{workflow_id}/start',
            path: {
                'workflow_id': workflowId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Start workflow component
     * @param workflowId
     * @param componentId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static startComponentApiV1WorkflowWorkflowIdStartComponentIdPost(
        workflowId: string,
        componentId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/workflow/{workflow_id}/start/{component_id}',
            path: {
                'workflow_id': workflowId,
                'component_id': componentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Reset workflow schema
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static resetWorkflowApiV1WorkflowWorkflowIdResetPost(
        requestBody: ResetWorkflowRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/workflow/{workflow_id}/reset',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get job state
     * @param jobId
     * @returns GetJobState Successful Response
     * @throws ApiError
     */
    public static getJobStateApiV1WorkflowJobJobIdStateGet(
        jobId: string,
    ): CancelablePromise<GetJobState> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/workflow/job/{job_id}/state',
            path: {
                'job_id': jobId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get state
     * @param componentId
     * @returns GetComponentResponse Successful Response
     * @throws ApiError
     */
    public static getComponentStateApiV1WorkflowComponentComponentIdStateGet(
        componentId: string,
    ): CancelablePromise<GetComponentResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/workflow/component/{component_id}/state',
            path: {
                'component_id': componentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
