/* Components */
'use client'

import { useGetAllFeedsQuery } from "@/lib/services/feed"

export default function Page() {
  const { data, error, isLoading } = useGetAllFeedsQuery()
  console.log(data)

  return (
    <div>
      {error ? (
        <>Oh no, there was an error</>
      ) : isLoading ? (
        <>Loading...</>
      ) : data ? (
        <>
          <h3>{data.results}</h3>
        </>
      ) : null}
    </div>
  )

}

export const metadata = {
  title: 'Second page',
}
