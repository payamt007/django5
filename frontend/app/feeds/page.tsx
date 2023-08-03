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

  interface DataType {
    key: React.Key;
    name: string;
    age: number;
    address: string;
}

  const data0: DataType[] = [
    {
        key: '1',
        name: 'John Brown',
        age: 32,
        address: 'New York No. 1 Lake Park',
    },
    {
        key: '2',
        name: 'Jim Green',
        age: 42,
        address: 'London No. 1 Lake Park',
    },
    {
        key: '3',
        name: 'Joe Black',
        age: 32,
        address: 'Sydney No. 1 Lake Park',
    },
    {
        key: '4',
        name: 'Disabled User',
        age: 99,
        address: 'Sydney No. 1 Lake Park',
    },
];

  return (
    <div>
      {error ? (
        <>Oh no, there was an error</>
      ) : isLoading ? (
        <>Loading...</>
      ) : data ? (
        <>
          <DataTable data={data0}/>
          <h3>{data.results}</h3>
        </>
      ) : null}
    </div>
  )

}

export const metadata = {
  title: 'Second page',
}
