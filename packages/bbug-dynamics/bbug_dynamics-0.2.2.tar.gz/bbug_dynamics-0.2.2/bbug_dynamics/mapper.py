from decimal import *
class Mapper():
    def __init__(self, source_entity, entities_map):
        self.source_entity=source_entity
        self.target_entity={}
        self.entities_map=entities_map
    def parse(self):
        for i in self.entities_map:
            if i=='__methods': continue
            self.target_entity[i]=self.get_value(self.entities_map[i])
        if '__methods' in self.entities_map:
            self.call_methods()
    def call_methods(self):
        methods=self.entities_map['__methods']
        for i in methods:
            if i['method']=='set_navigation_property':
                self.target_entity[i['field']]=i['uri'] + '(' + self.get_value(i['value']) + ')'
            elif i['method']=='set_value':
                self.target_entity[i['field']]=i['value']
            elif i['method']=='replace_substring':
                self.target_entity[i['field']]=self.get_value(i['value']).replace(i['search'],i['replace_by'])
            else:
                raise BaseException("The method: " + i['method'] + " is not defined")

    def get_value(self,value):
        final_value = self.source_entity
        for field in value.split('.'):
            if field.startswith('__'):
                if field=='__first':
                    final_value=final_value[0]
            else:
                final_value= '' if field not in final_value else final_value[field]
        final_value = int(final_value) if final_value.__class__.__name__=='Decimal' else final_value
        return final_value
