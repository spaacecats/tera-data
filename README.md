# tera-data

This repository is intended to house packet and system message information for
TERA. It is intended to be platform agnostic, with details on the file formats
explained below.

The current, known open source parsers are:
- JavaScript (Node): [tera-data-parser](https://github.com/meishuu/tera-data-parser-js)

## Mappings

The `map` directory contains files which map unique identifiers (names) to their
numeric values. Currently, this includes:

- `protocol.map`, which links opcodes to "packet" names
- `sysmsg.map`, which links system message IDs to readable names

These generally come from the client binary and should not be built or modified
by hand unless you know what you're doing.

Methods and instructions on dumping opcodes and sysmsgs can be found from:
- [Meishu](https://github.com/meishuu/TeraScanners)
- [Gl0](https://github.com/neowutran/TeraDpsMeterData/blob/master/copypaste-tuto/Gl0-opcodes.txt)
- [GoneUp](https://github.com/GoneUp/Tera_PacketViewer/tree/master/Opcode%20DLL#readme)

## Protocol

TERA's network data follows a custom protocol. It is convenient to describe the
order and meaning of each element in a "packet", which is done through a `.def`
file under the `protocol` directory, and named after the opcode it belongs to.

Each line in the `.def` must consist of the following, in order:
- An optional series of `-` for array definitions. These may be separated by
  spaces. To nest arrays, just add another `-` to the front.
- A field type. Valid types listed below.
- At least one space.
- The name of the field.

A `#` and anything after it on the line are treated as comments and will be
ignored when parsing.

The following basic field types are supported:
- `byte`: A single byte. Also used for booleans.
- `float`
- `int16`
- `int32`
- `int64`
- `uint16`
- `uint32`
- `uint64`

The protocol also supports variable-length fields, along with accompanying
metadata. These are described with the following field types:
- `count`: Acts as `uint16`. Dictates the length of an `array` or `bytes` field
  of the same name.
- `offset`: Acts as `uint16`. Indicates the byte offset from the beginning of
  the message for an `array`, `bytes`, or `string` field of the same name.
- `array`: Requires both `count` and `offset`.
- `bytes`: A series of `byte` data. Requires both `count` and `offset`.
- `string`: String data, treated as a null-terminated series of `uint16`. Only
  uses `offset` metadata.

More details on the original message format are below, while details on your
language's or library's implementation of these types should be described in
your library's documentation.

### Message Format

TERA's networking encodes all data in little-endian.

There are a few fields which are implied because they are never omitted. Every
packet begins with two fields:
- `uint16 length`, which describes the byte length of the message, including
  this header.
- `uint16 opcode`, which describes which kind of message this is. By looking up
  which name has this number in the mapping, you will know what the message is
  called.

Additionally, all array elements begin with two fields:
- `offset here`, which can be used to verify correctness. If this is the first
  element, the `offset` for the array should match this; otherwise, it should
  match the `next` for the previous element.
- `offset next`, which points to the byte offset of the next element in the
  array, or zero if this is the final element.

In general, you will find `count` and `offset` fields at the beginning of a
message or array definition, and their corresponding fields at the end. See
`protocol/S_SPAWN_USER.def` for an example.
