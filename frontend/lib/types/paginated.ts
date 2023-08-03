import { feedType } from "./feeds"

export type paginatedResult = {
    count: number,
    next: number | null,
    previous: number | null,
    results: any[]
}

export type paginatedFeedType = {
    count: number,
    next: number | null,
    previous: number | null,
    results: feedType[]
}