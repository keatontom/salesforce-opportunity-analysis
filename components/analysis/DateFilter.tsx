import { Button } from "@/components/ui/button"

export type DateRange = 'all' | 'q1' | 'q2' | 'q3' | 'q4' | 'ytd' | 'last_year'

interface DateFilterProps {
  selected: DateRange;
  onChange: (range: DateRange) => void;
}

const DATE_OPTIONS: { value: DateRange; label: string }[] = [
  { value: 'ytd', label: 'Year to Date' },
  { value: 'q4', label: 'Q4' },
  { value: 'q3', label: 'Q3' },
  { value: 'q2', label: 'Q2' },
  { value: 'q1', label: 'Q1' },
  { value: 'last_year', label: 'Last Year' },
  { value: 'all', label: 'All Time' },
]

export default function DateFilter({ selected, onChange }: DateFilterProps) {
  return (
    <div className="flex flex-wrap gap-2">
      {DATE_OPTIONS.map(({ value, label }) => (
        <Button
          key={value}
          variant={selected === value ? "default" : "outline"}
          size="sm"
          onClick={() => onChange(value)}
        >
          {label}
        </Button>
      ))}
    </div>
  )
}