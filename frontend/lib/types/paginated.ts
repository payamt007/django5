export type paginatedResult = {
    count: number,
    next: number | null,
    previous: number | null,
    results: any[]
}