def event_to_series(event_data, label_name="txns"):
    """
    FROM:
    OrderedDict([('id', '0x34fbb92e0c0bd6f50bb637467fd720f923c6acd3df434dc04c1757dd4d9cb1a0'),
                 ('collection_slug', 'adam-bomb-squad'),
                 ('buyer_address', '0x531841ddbda6dc08619bc7fb73f2605275be26c8'), ...

    TO:
    const data: Series[] = [
      {
        label: 'txns",
        data: [
          {
            date: new Date(),
            stars: 202123,
          }
          // ...
        ]
      },
      {
        label: 'React Query",
        data: [
          {
            date: new Date(),
            stars: 10234230,
          }
          // ...
        ]
      }
    ]
    """
    my_series = []
    table = {"label": label_name, "data": []}
    for event in event_data:
        curr_table = {}
        for label in event:
            curr_table[label] = event[label]
            table["data"].append(curr_table)
    my_series.append(table)
    return my_series

    # convert table format {label: [list,of,data], label2: [list,of,dat]} to series format [{label: label, data: [list,of,data]},{},...]
