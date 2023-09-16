import {createApi, fetchBaseQuery} from '@reduxjs/toolkit/query/react'
import {paginatedFeedType} from '../types/paginated'
import {feedType} from '../types/feeds'
import {generalResponseType, loginTokenType} from '../types/login';
import React from 'react';

// Define a service using a base URL and expected endpoints
export const feedsApi = createApi({
    reducerPath: 'feedApi',
    baseQuery: fetchBaseQuery({baseUrl: 'http://127.0.0.1:8000/'}),
    tagTypes: ['Feeds', 'login'],
    endpoints: (build) => ({
        login: build.mutation<generalResponseType, { username: string, password: string }>({
            query: ({username, password}) => ({
                url: `auth/token/`,
                method: 'POST',
                body: {username, password},
            }),
            // transformResponse: (response: loginTokenType, meta,
            //                     arg) => response.access as loginTokenType,
            transformResponse: (response: generalResponseType, meta,
                                arg) => response,
            transformErrorResponse: (
                response: { status: string | number },
                meta,
                arg
            ) => response.status,
        }),
        getAllFeeds: build.query<paginatedFeedType, void>({
            query: () => 'api/feeds',
            providesTags: ['Feeds'],
        }),
        createFeed: build.mutation<void, Pick<feedType, 'title' | 'link'>>({
            // note: an optional `queryFn` may be used in place of `query`
            query: ({...body}) => ({
                url: 'api/feeds/',
                method: 'POST',
                body: body,
            }),
            // Pick out data and prevent nested properties in a hook or selector
            transformResponse: (response: { data: void }, meta, arg) => response.data,
            // Pick out errors and prevent nested properties in a hook or selector
            transformErrorResponse: (
                response: { status: string | number },
                meta,
                arg
            ) => response.status,
            invalidatesTags: ['Feeds'],
            // onQueryStarted is useful for optimistic updates
            // The 2nd parameter is the destructured `MutationLifecycleApi`
            async onQueryStarted(
                arg,
                {dispatch, getState, queryFulfilled, requestId, extra, getCacheEntry}
            ) {
            },
            // The 2nd parameter is the destructured `MutationCacheLifecycleApi`
            async onCacheEntryAdded(
                arg,
                {
                    dispatch,
                    getState,
                    extra,
                    requestId,
                    cacheEntryRemoved,
                    cacheDataLoaded,
                    getCacheEntry,
                }
            ) {
            },
        }),
        updateFeed: build.mutation<void, { id: number; body: Partial<feedType> }>({
            query: ({id, body}) => {
                return {
                    url: `api/feeds/${id}/`,
                    method: 'PATCH',
                    body: body,
                }
            },
            // Pick out data and prevent nested properties in a hook or selector
            transformResponse: (response: { data: void }, meta, arg) => response.data,
            // Pick out errors and prevent nested properties in a hook or selector
            transformErrorResponse: (
                response: { status: string | number },
                meta,
                arg
            ) => response.status,
            invalidatesTags: ['Feeds'],
            // onQueryStarted is useful for optimistic updates
            // The 2nd parameter is the destructured `MutationLifecycleApi`
            async onQueryStarted(
                arg,
                {dispatch, getState, queryFulfilled, requestId, extra, getCacheEntry}
            ) {
            },
            // The 2nd parameter is the destructured `MutationCacheLifecycleApi`
            async onCacheEntryAdded(
                arg,
                {
                    dispatch,
                    getState,
                    extra,
                    requestId,
                    cacheEntryRemoved,
                    cacheDataLoaded,
                    getCacheEntry,
                }
            ) {
            },
        }),
        deleteFeed: build.mutation<void, { keys: React.Key[] }>({
            query: (keys) => {
                return {
                    url: 'api/delete-feeds',
                    method: 'DELETE',
                    body: keys,
                }
            },
            // Pick out data and prevent nested properties in a hook or selector
            //transformResponse: (response: { data: void }, meta, arg) => response.data,
            // Pick out errors and prevent nested properties in a hook or selector
            transformErrorResponse: (
                response: { status: string | number },
                meta,
                arg
            ) => response.status,
            invalidatesTags: ['Feeds'],
            // onQueryStarted is useful for optimistic updates
            // The 2nd parameter is the destructured `MutationLifecycleApi`
            async onQueryStarted(
                arg,
                {dispatch, getState, queryFulfilled, requestId, extra, getCacheEntry}
            ) {
            },
            // The 2nd parameter is the destructured `MutationCacheLifecycleApi`
            async onCacheEntryAdded(
                arg,
                {
                    dispatch,
                    getState,
                    extra,
                    requestId,
                    cacheEntryRemoved,
                    cacheDataLoaded,
                    getCacheEntry,
                }
            ) {
            },
        }),
    })
})


// Export hooks for usage in functional components, which are
// auto-generated based on the defined endpoints
export const {
    useLoginMutation,
    useGetAllFeedsQuery,
    useCreateFeedMutation,
    useUpdateFeedMutation,
    useDeleteFeedMutation
} = feedsApi