/* Components */
'use client'

import { useGetAllFeedsQuery } from "@/lib/services/feed"
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';
import DataTable from "@/app/components/Table"

const columns: GridColDef[] = [
  { field: 'id', headerName: 'ID', width: 70 },
  { field: 'title', headerName: 'Title', width: 130 },
  { field: 'link', headerName: 'Link', width: 130 },
  { field: 'followed', headerName: 'Followed', width: 20 },
  { field: 'stopeed', headerName: 'Stopeed', width: 20 },
  { field: 'fails', headerName: 'Fails', width: 20 },
];

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
          <DataTable />
          <h3>{data.results}</h3>
        </>
      ) : null}
    </div>
  )

}

export const metadata = {
  title: 'Second page',
}
