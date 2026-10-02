SQL_CONFIG = {
    "server": "172.16.1.31",
    "database": "NVHUSA_REAL",
    "username": "cleber",
    "password": "cleber",
}

CLICKHOUSE_CONFIG = {
    "host": "localhost",
    "port": 8123,
    "username": "default",
    "password": "clickhouse",
    "database": "mes"
}

TABLES = [

    {
        "source_table": "InventoryStatus",
        "target_table": "DAILY_INVENTORY_INOUT_SUMMARY"
    },

    {
        "source_table": "DeliveryStatus",
        "target_table": "DELIVERY_LOT"
    },

    {
        "source_table": "ShippingStatus",
        "target_table": "SHIPMENT_ID_STS"
    },

    {
        "source_table": "ServiceHistory",
        "target_table": "SYS_SERVICE_INOUT_PARAMS"
    }

]
