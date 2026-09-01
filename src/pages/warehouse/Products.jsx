import ApiResourceTable from '../../components/ApiResourceTable';

function Products() {
  return <ApiResourceTable title="Product Catalog" description="Live products from the warehouse API." endpoint="warehouse/products/" columns={[{ key: 'product_id', label: 'ID' }, { key: 'product_code', label: 'Code' }, { key: 'product_name', label: 'Name' }, { key: 'category', label: 'Category' }, { key: 'status', label: 'Status' }]} searchKeys={['product_code', 'product_name', 'status']} />;
}

export default Products;
