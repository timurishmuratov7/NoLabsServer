/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExperimentMetadataResponse } from '../models/ExperimentMetadataResponse';
import type { UpdateExperimentRequest } from '../models/UpdateExperimentRequest';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ExperimentsService {
    /**
     * Get all experiments
     * @returns ExperimentMetadataResponse Successful Response
     * @throws ApiError
     */
    public static experimentsApiV1ExperimentsAllGet(): CancelablePromise<Array<ExperimentMetadataResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/experiments/all',
        });
    }
    /**
     * Delete experiment
     * @param experimentId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteExperimentApiV1ExperimentsExperimentIdDelete(
        experimentId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/experiments/{experiment_id}',
            path: {
                'experiment_id': experimentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create experiment
     * @returns ExperimentMetadataResponse Successful Response
     * @throws ApiError
     */
    public static createExperimentApiV1ExperimentsPost(): CancelablePromise<ExperimentMetadataResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/experiments/',
        });
    }
    /**
     * Update experiment
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static updateExperimentApiV1ExperimentsPatch(
        requestBody: UpdateExperimentRequest,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/experiments/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
