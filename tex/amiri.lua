amiri = { }

amiri.module     = {
    name        = "amiri",
    version     = 0.001,
    date        = "2011/04/16",
    description = "Support module for Amiri font",
    author      = "Khaled Hosny",
    copyright   = "Khaled Hosny",
    license     = "CC0",
}

if not modules then modules = { } end modules ['amiri'] = amiri.module

local code_attr, id_attr

if context then
    code_attr = attributes.private("amiricharcode")
    id_attr   = attributes.private("amiricharid")
else
    code_attr = luatexbase.new_attribute("amiricharcode")
    id_attr   = luatexbase.new_attribute("amiricharid")
end

local glyph     = node.id("glyph")
local hlist     = node.id("hlist")
local vlist     = node.id("vlist")
local glue      = node.id("glue")

local format    = string.format

-- XXX
local ids       = fonts.hashes and fonts.hashes.identifiers or fonts.ids

local function is_amiri(font)
    font = ids[font]
    font = font and font.shared
    font = font and (font.rawdata or font.otfdata) -- XXX
    font = font and font.metadata
    font = font and font.familyname
    if font == "Amiri" then
        return true
    else
        return false
    end
end

local charid = 0

local function initialise(head)
    for n in node.traverse(head) do
        if n.id == glyph and is_amiri(n.font) then
            charid = charid + 1
            node.set_attribute(n, id_attr,   charid)
            node.set_attribute(n, code_attr, n.char)
        end
    end
    return head
end

local function tosixteen(code)
    if not code then
        return "<feff>"
    else
        r = {}
        for _,n in next, code do
            if n < 0x10000 then
                r[#r+1] = format("%04x",n)
            else
                r[#r+1] = format("%04x%04x",n/1024+0xD800,n%1024+0xDC00)
            end
        end
        return format("<feff%s>", table.concat(r))
    end
end

local function new_actualtext(code)
    local actualtext = node.new(node.id("whatsit"), 8)
    actualtext.mode = 1
    if code then
        actualtext.data = format("/Span << /ActualText %s >> BDC", tosixteen(code))
    else
        actualtext.data = "EMC"
    end
    return actualtext
end

local function finalise_char(head)
    for n in node.traverse(head) do
        if n.id == glyph and is_amiri(n.font) then
            local id   = node.has_attribute(n, id_attr)
            local code = node.has_attribute(n, code_attr)
            if n.prev and n.prev.id == glyph and node.has_attribute(n.prev, id_attr) == id then
            else
                local b = new_actualtext({code})
                node.insert_before(head, n, b)
            end
            if n.next and n.next.id == glyph and node.has_attribute(n.next, id_attr) == id then
            else
                local e = new_actualtext()
                node.insert_after(head, n, e)
            end
        elseif n.id == hlist or n.id == vlist then
            amiri.finalise(n.list)
        end
    end
    return head
end

local function finalise_word(head)
    local start, id, code = nil, nil, {}
    for n in node.traverse(head) do
        if n.id == glyph and is_amiri(n.font) then
            local i = node.has_attribute(n, id_attr)
            local c = node.has_attribute(n, code_attr)
            if i ~= id then
                code[#code+1] = c
            end
            id = i
            if not start then
                start = n
            end
        elseif n.id == glue then
            if start then
                local b = new_actualtext(code)
                local e = new_actualtext()
                node.insert_before(head, start, b)
                node.insert_after(head, n, e)
                start, code = nil, {}
            end
        elseif n.id == hlist or n.id == vlist then
            amiri.finalise(n.list)
        end
    end
    return head
end

amiri.finalise   = finalise_word
amiri.initialise = initialise
